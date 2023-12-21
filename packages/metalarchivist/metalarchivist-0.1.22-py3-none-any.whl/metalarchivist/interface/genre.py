import re
from enum import StrEnum, auto
from dataclasses import dataclass, field, InitVar

import lxml.html

from .base import PageDataType, Period



class SubgenrePeriod(Period):
    ...


class Genre(StrEnum):
    BLACK = auto()
    DEATH = auto()
    DOOM = auto()
    AVANTGARDE = auto()
    FOLK = auto()
    GOTHIC = auto()
    GRIND = auto()
    GROOVE = auto()
    HEAVY = auto()
    METALCORE = auto()
    POWER = auto()
    PROG = auto()
    SPEED = auto()
    ORCHESTRAL = auto()
    THRASH = auto()


class GenreJunk(StrEnum):
    METAL = auto()
    ELEMENTS = auto()
    INFLUENCES = auto()
    MUSIC = auto()
    AND = auto()
    WITH = auto()

    @classmethod
    def has_value(cls, value) -> bool:
        return value.lower() in cls._value2member_map_
    

@dataclass(frozen=True)
class SubgenrePhase:
    name: str
    period: SubgenrePeriod = field(default=SubgenrePeriod.ALL)


@dataclass
class BandGenre(PageDataType):
    genre_page_record: InitVar[list[str]]
    profile_url: str = field(init=False)
    subgenre: str = field(init=False)
    genre: str = field(kw_only=True)

    def __post_init__(self, genre_page_record: list[str]):
        profile_anchor_text, _, subgenre, _ = genre_page_record

        profile_anchor = lxml.html.fragment_fromstring(profile_anchor_text)
        self.profile_link = profile_anchor.attrib['href']
        self.subgenre = subgenre.replace(' Metal', '').strip()


@dataclass
class Subgenres:
    """ Handle genres specified in text assuming 
        the conventions applied by metal-archives.com
        
        Phases: separated by semicolons (;), denotes a change
            in a bands sound over a series of periods wrapped in
            parentheses, *early*, *mid*, and *later*. See `GenrePhase`.

            *e.g* Doom Metal (early); Post-Rock (later)

        Multiples: A slash (/) indicates that a band fits within
            multiple genres. Phases are subdivided into multiples,
            where applicable. Bands without phases will likewise
            contain multiples.

            *e.g* Drone/Doom Metal (early); Psychedelic/Post-Rock (later),
                Progressive Death/Black Metal

        Modifiers: A genre can be modified into a variant with descriptive
            text, delimited by a space ( ).

            *e.g* Progressive Death Metal

        Junk: Words that are largely uninformative can be removed, the most
            common being "Metal". See `GenreJunk`.

            *e.g* Symphonic Gothic Metal with Folk influences
    """

    full_genre: str
    clean_genre: str = field(init=False)
    phases: list[SubgenrePhase] = field(init=False)

    def __post_init__(self):
        # scrub anomalies
        clean_genre = re.sub(r' Metal', '', self.full_genre)
        clean_genre = re.sub(r'\b \'n\' \b', '\'n\'', self.full_genre)
        clean_genre = re.sub(r'\u200b', '', clean_genre)
        clean_genre = re.sub(chr(1089), chr(99), clean_genre)
        clean_genre = re.sub(r'(\w)\(', r'\g<1> (', clean_genre)
        clean_genre = re.sub(r'\)\/? ', r'); ', clean_genre)
        clean_genre = re.sub(r' \- ', ' ', clean_genre)

        phases = clean_genre.split(';')

        # strip and use regex to parse genre phase components
        phases = list(map(self._parse_phase, map(str.lstrip, phases)))

        # explode strings into multiple records by character
        phases = self._explode_phases_on_delimiter(phases, '/')
        phases = self._explode_phases_on_delimiter(phases, ',')

        # remove meaningless text
        phases = self._scrub_phases_of_junk(phases)

        # convert genres that appear in all phases to a single ALL record
        phases = self._collapse_recurrent_phases(phases)

        self.phases = phases = list(set(phases))
        sorted_genres = sorted(phases, key=self._phase_sort_key)
        self.clean_genre = ', '.join(map(lambda n: n.name, sorted_genres))

    @staticmethod
    def _phase_sort_key(phase: SubgenrePhase):
        return (SubgenrePeriod._member_names_.index(phase.period.name), phase.name)

    @staticmethod
    def _collapse_recurrent_phases(phases: list[SubgenrePhase]) -> list[SubgenrePhase]:
        total_phases = len(set(map(lambda n: n.period, phases)))

        phase_counts = dict()
        for phase in phases:
            try:
                phase_counts[phase.name] += 1
            except KeyError:
                phase_counts[phase.name] = 1

        consistent_genres = set(g for g, c in phase_counts.items() if c == total_phases)
        collapsed_phases = list(map(SubgenrePhase, consistent_genres)) 
        collapsed_phases += list(filter(lambda p: p.name not in consistent_genres, phases))

        return collapsed_phases

    @staticmethod
    def _scrub_phases_of_junk(phases: list[SubgenrePhase]) -> list[SubgenrePhase]:
        def scrub(phase):
            return [SubgenrePhase(p, phase.period)
                    for p in phase.name.split(' ')
                    if not GenreJunk.has_value(p)]
        
        return sum(list(map(scrub, phases)), [])

    @staticmethod
    def _explode_phases_on_delimiter(phases: list[SubgenrePhase], delimiter: str) -> list[SubgenrePhase]:
        def explode(phase):
            return [SubgenrePhase(n.strip(), phase.period) for n in phase.name.split(delimiter)]
            
        return sum(list(map(explode, phases)), [])

    @staticmethod
    def _parse_phase(phase: str) -> SubgenrePhase:
        phase_match = re.compile(r'^(?P<name>.*?)(\((?P<period>[\w\/\, ]+)\))?$').match(phase)
        
        phase_record = phase_match.groupdict() if phase_match else dict(name=phase, period='all')
        try:
            period = phase_record['period']
            phase_record['period'] = SubgenrePeriod[period.upper()] if period else SubgenrePeriod.ALL
        except KeyError:
            phase_record['period'] = SubgenrePeriod.ERROR

        return SubgenrePhase(**phase_record)
    
    def to_dict(self) -> dict:
        phases = [dict(name=p.name.lower(), period=p.period.value) for p in self.phases]
        return dict(genre=self.clean_genre.lower(), genre_phases=phases)
