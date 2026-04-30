import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar


class ProviderName(Enum):
    """Canonical provider names."""

    ABC_IVIEW = "ABC iview"
    ACONTRA_PLUS = "Acontra Plus"
    ACONTRA_PLUS_AMAZON_CHANNEL = "Acontra Plus Amazon Channel"
    ACORNTV = "AcornTV"
    ACORNTV_AMAZON_CHANNEL = "AcornTV Amazon Channel"
    ACORNTV_APPLE_TV = "Acorn TV Apple TV"
    ACTION_MAX_AMAZON_CHANNEL = "Action Max Amazon Channel"
    ALLENTE = "Allente"
    ALLESKINO = "Alleskino"
    ALLESKINO_AMAZON_CHANNEL = "Alleskino Amazon Channel"
    AMAZON_PRIME_VIDEO = "Amazon Prime Video"
    AMC = "AMC"
    AMC_CHANNELS_AMAZON_CHANNEL = "AMC Channels Amazon Channel"
    AMC_PLUS = "AMC+"
    AMC_PLUS_AMAZON_CHANNEL = "AMC+ Amazon Channel"
    AMC_PLUS_APPLE_TV_CHANNEL = "AMC Plus Apple TV Channel"
    AMC_PLUS_ROKU_PREMIUM_CHANNEL = "AMC+ Roku Premium Channel"
    APPLE_TV = "Apple TV"
    APPLE_TV_PLUS = "Apple TV+"
    ARD_PLUS = "ARD Plus"
    ARD_PLUS_AMAZON_CHANNEL = "ARD Plus Amazon channel"
    ARD_PLUS_APPLE_TV_CHANNEL = "ARD Plus Apple TV channel"
    ARTE_BOUTIQUE = "ARTE Boutique"
    ARTHOUSE_CNMA = "ArthouseCNMA"
    ARTHOUSE_CNMA_AMAZON_CHANNEL = "Arthouse CNMA Amazon Channel"
    ASIANCRUSH = "AsianCrush"
    ATRES_PLAYER = "Atres Player"
    BBC_IPLAYER = "BBC iPlayer"
    BBOX_VOD = "Bbox VOD"
    BEAMAFILM = "Beamafilm"
    BELAS_ARTES_A_LA_CARTE = "Belas Artes à La Carte"
    BE_TV_GO = "Be TV Go"
    BFI_PLAYER = "BFI Player"
    BFI_PLAYER_AMAZON_CHANNEL = "BFI Player Amazon Channel"
    BFI_PLAYER_APPLE_TV_CHANNEL = "BFI Player Apple TV Channel"
    BINGE = "BINGE"
    BLOCKBUSTER = "Blockbuster"
    BLOODY_MOVIES_AMAZON_CHANNEL = "Bloody Movies Amazon Channel"
    BLUE_TV = "blue TV"
    BROADWAYHD = "BroadwayHD"
    BRITBOX = "BritBox"
    BRITBOX_AMAZON_CHANNEL = "BritBox Amazon Channel"
    BRITBOX_APPLE_TV_CHANNEL = "BritBox Apple TV Channel"
    CANAL_PLUS = "Canal+"
    CANAL_VOD = "Canal VOD"
    CATCHPLAY = "Catchplay"
    CDA_PREMIUM = "CDA Premium"
    CG_TV_STREAMING = "CG TV STREAMING"
    CHANNEL_4_PLUS = "Channel 4 Plus"
    CHILI = "CHILI"
    CINEASTERNA = "Cineasterna"
    CINEMAS_A_LA_DEMANDE = "Cinemas a la Demande"
    CINEMAX_AMAZON_CHANNEL = "Cinemax Amazon Channel"
    CINEMAX_APPLE_TV_CHANNEL = "Cinemax Apple TV Channel"
    CINEMEMBER = "CineMember"
    CINE_PLUS_OCS_AMAZON_CHANNEL = "Cine+ OCS Amazon Channel"
    CINOBO = "Cinobo"
    CINU = "Cinu"
    CLARO_TV_PLUS = "Claro tv+"
    CLARO_VIDEO = "Claro video"
    CLUB_ILLICO = "Club Illico"
    COSMOGO = "CosmoGo"
    CRAVE = "Crave"
    CRAVE_AMAZON_CHANNEL = "Crave Amazon Channel"
    CRITERION_CHANNEL = "Criterion Channel"
    CRUNCHYROLL = "Crunchyroll"
    CRUNCHYROLL_AMAZON_CHANNEL = "Crunchyroll Amazon Channel"
    CULTPIX = "Cultpix"
    CURIOSITY_STREAM = "Curiosity Stream"
    CURIOSITY_STREAM_AMAZON_CHANNEL = "Curiosity Stream Amazon Channel"
    CURIOSITY_STREAM_APPLE_TV_CHANNEL = "Curiosity Stream Apple TV Channel"
    CURZON_HOME_CINEMA = "Curzon Home Cinema"
    CURZON_AMAZON_CHANNEL = "Curzon Amazon Channel"
    DANIME_AMAZON_CHANNEL = "dAnime Amazon Channel"
    DISCOVERY_PLUS = "Discovery+"
    DISCOVERY_PLUS_AMAZON_CHANNEL = "Discovery+ Amazon Channel"
    DISNEY_PLUS = "Disney Plus"
    DISNEY_PLUS_AMAZON_CHANNEL = "Disney+ Amazon Channel"
    DOCPLAY = "DocPlay"
    DOCPLAY_AMAZON_CHANNEL = "DocPlay Amazon Channel"
    DOCSVILLE = "DOCSVILLE"
    DOCURAMAFILMS_AMAZON_CHANNEL = "DocuramaFilms Amazon Channel"
    DRAKEN_FILMS = "Draken Films"
    ELISA_VIIHDE = "Elisa Viihde"
    ETERNAL_FAMILY = "Eternal Family"
    FANDANGO_AT_HOME = "Fandango At Home"
    FANDOR_AMAZON_CHANNEL = "Fandor Amazon Channel"
    FAR_EAST_AMAZON_CHANNEL = "Far East Amazon Channel"
    FAWESOME = "Fawesome"
    FETCH_TV = "Fetch TV"
    FILMBOX_PLUS = "FilmBox+"
    FILMIN = "Filmin"
    FILMINGO = "Filmingo"
    FILMO = "FILMO"
    FILMOTEKET = "Filmoteket"
    FILMSTRIBEN = "Filmstriben"
    FLIXFLING = "FlixFling"
    FLIXHOUSE = "FlixHouse"
    FLIXOLE = "FlixOlé"
    FLIXOLE_AMAZON_CHANNEL = "FlixOlé Amazon Channel"
    FLIXOLE_APPLE_TV_CHANNEL = "FlixOlé Apple TV Channel"
    FOD = "FOD"
    FOD_CHANNEL_AMAZON_CHANNEL = "FOD Channel Amazon Channel"
    FOXTEL_NOW = "Foxtel Now"
    FREENET_MEINVOD = "Freenet meinVOD"
    FUBOTV = "fuboTV"
    FXNOW = "FXNow"
    GALACTIC_STREAM_AMAZON_CHANNEL = "Galactic Stream Amazon Channel"
    GLOBOPLAY = "Globoplay"
    GO3 = "Go3"
    GOOGLE_PLAY_MOVIES = "Google Play Movies"
    GUIDEDOC = "GuideDoc"
    HBO_MAX = "HBO Max"
    HBO_MAX_AMAZON_CHANNEL = "HBO Max Amazon Channel"
    HBO_MAX_ON_U_NEXT = "HBO Max on U-Next"
    HISTORAMA = "Historama"
    HISTORAMA_AMAZON_CHANNEL = "Historama Amazon Channel"
    HISTORAMA_APPLE_TV_CHANNEL = "Historama Apple TV Channel"
    HOICHOI = "Hoichoi"
    HOICHOI_AMAZON_CHANNEL = "Hoichoi Amazon Channel"
    HOICHOI_APPLE_TV_CHANNEL = "Hoichoi Apple TV Channel"
    HOLLYWOOD_SUITE = "Hollywood Suite"
    HOLLYWOOD_SUITE_AMAZON_CHANNEL = "Hollywood Suite Amazon Channel"
    HOME_OF_HORROR = "Home of Horror"
    HOME_OF_HORROR_AMAZON_CHANNEL = "Home of Horror Amazon Channel"
    HOOPLA = "Hoopla"
    HOTSTAR = "Hotstar"
    HULU = "Hulu"
    HUNGAMA_PLAY = "Hungama Play"
    ICITOUTV = "iciTouTV"
    IFLIX = "iflix"
    INFINITY_SELECTION_AMAZON_CHANNEL = "Infinity Selection Amazon Channel"
    ITVX_PREMIUM = "ITVX Premium"
    IWONDER_FULL_AMAZON_CHANNEL = "iWonder Full Amazon Channel"
    JIOHOTSTAR = "JioHotstar"
    JOYN = "Joyn"
    JOYN_PLUS = "Joyn Plus"
    JUSTWATCHTV = "JustWatchTV"
    KANOPY = "Kanopy"
    KINO_ON_DEMAND = "Kino on Demand"
    KINOPOISK = "Kinopoisk"
    KIRJASTOKINO = "Kirjastokino"
    KPN = "KPN"
    LACINETEK = "LaCinetek"
    LEPSI_TV = "Lepsi TV"
    LINE_TV = "LINE TV"
    LIONSGATE_PLAY = "Lionsgate Play"
    LIONSGATE_PLAY_AMAZON_CHANNEL = "Lionsgate Play Amazon Channel"
    LIONSGATE_PLAY_APPLE_TV_CHANNEL = "Lionsgate Play Apple TV Channel"
    LIONSGATE_PLUS_AMAZON_CHANNELS = "Lionsgate+ Amazon Channels"
    MAGELLAN_TV = "Magellan TV"
    MAGENTA_TV = "MagentaTV"
    MAGENTA_TV_PLUS = "Magenta TV+"
    MAXDOME_STORE = "maxdome Store"
    MEJANE = "meJane"
    MERCADO_PLAY = "Mercado Play"
    MGM_PLUS = "MGM Plus"
    MGM_PLUS_AMAZON_CHANNEL = "MGM+ Amazon Channel"
    MGM_PLUS_ROKU_PREMIUM_CHANNEL = "MGM Plus Roku Premium Channel"
    MIDNIGHT_FACTORY_AMAZON_CHANNEL = "MIDNIGHT FACTORY Amazon Channel"
    MIDNIGHT_PULP = "Midnight Pulp"
    MIDNIGHT_PULP_AMAZON_CHANNEL = "Midnight Pulp Amazon Channel"
    MOLOTOV_TV = "Molotov TV"
    MORE_TV = "More TV"
    MOVISTARTV = "MovistarTV"
    MOVISTAR_PLUS = "Movistar Plus+"
    MOVISTAR_PLUS_FICCION_TOTAL = "Movistar Plus+ Ficción Total"
    MTV_KATSOMO = "MTV Katsomo"
    MUBI = "MUBI"
    MUBI_AMAZON_CHANNEL = "MUBI Amazon Channel"
    MYMOVIES_ONE = "MYmovies One"
    NEON_TV = "Neon TV"
    NETFLIX = "Netflix"
    NETZKINO = "Netzkino"
    NIGHT_FLIGHT_PLUS = "Night Flight Plus"
    NOW_TV = "Now TV"
    NOW_TV_CINEMA = "Now TV Cinema"
    OKKO = "Okko"
    OLDFLIX = "Oldflix"
    ONEPLAY = "Oneplay"
    ORANGE_VOD = "Orange VOD"
    OSN_PLUS = "OSN+"
    OVID = "OVID"
    OZFLIX = "OzFlix"
    PARAMOUNT_PLUS = "Paramount Plus"
    PARAMOUNT_PLUS_AMAZON_CHANNEL = "Paramount+ Amazon Channel"
    PARAMOUNT_PLUS_APPLE_TV_CHANNEL = "Paramount Plus Apple TV Channel"
    PARAMOUNT_PLUS_ROKU_PREMIUM_CHANNEL = "Paramount+ Roku Premium Channel"
    PATHE_HOME = "Pathé Home"
    PATHE_THUIS = "Pathé Thuis"
    PEACOCK = "Peacock"
    PHILO = "Philo"
    PILOT_WP = "Pilot WP"
    PLAYER = "Player"
    PLEX = "Plex"
    PLEX_CHANNEL = "Plex Channel"
    POLSAT_BOX_GO = "Polsat Box Go"
    PREMIERE_MAX = "Premiere Max"
    PREMIERY_CANAL_PLUS = "Premiery Canal+"
    PRIMA_PLUS = "Prima Plus"
    QUEENS_CLUB = "Queens Club"
    QUEENS_CLUB_AMAZON_CHANNEL = "Queens Club Amazon Channel"
    RAKUTEN_TV = "Rakuten TV"
    RESERVA_IMOVISION_AMAZON_CHANNEL = "Reserva Imovision Amazon Channel"
    RETROCRUSH = "Retrocrush"
    RETROCRUSH_AMAZON_CHANNEL = "RetroCrush Amazon Channel"
    REVEEL = "Reveel"
    RTBF_AUVIO = "RTBF Auvio"
    RTL_PLUS = "RTL+"
    RTL_PLUS_MAX_AMAZON_CHANNEL = "RTL+ Max Amazon Channel"
    RUUTU = "Ruutu"
    SF_ANYTIME = "SF Anytime"
    SHADOWZ = "Shadowz"
    SHADOWZ_AMAZON_CHANNEL = "Shadowz Amazon Channel"
    SHAHID_VIP = "Shahid VIP"
    SHOWMAX = "ShowMax"
    SHUDDER = "Shudder"
    SHUDDER_AMAZON_CHANNEL = "Shudder Amazon Channel"
    SHUDDER_APPLE_TV_CHANNEL = "Shudder Apple TV Channel"
    SKY = "Sky"
    SKYSHOWTIME = "SkyShowtime"
    SKY_GO = "Sky Go"
    SKY_STORE = "Sky Store"
    SKY_X = "Sky X"
    SONY_LIV = "Sony Liv"
    SONY_ONE_AMAZON_CHANNEL = "Sony One Amazon Channel"
    SONY_PICTURES_AMAZON_CHANNEL = "Sony Pictures Amazon Channel"
    SOONER = "Sooner"
    SPECTRUM_ON_DEMAND = "Spectrum On Demand"
    STAN = "Stan"
    STARZ = "Starz"
    STARZPLAY = "STARZPLAY"
    STARZ_AMAZON_CHANNEL = "Starz Amazon Channel"
    STARZ_APPLE_TV_CHANNEL = "Starz Apple TV Channel"
    STARZ_ROKU_PREMIUM_CHANNEL = "Starz Roku Premium Channel"
    STRIM = "Strim"
    STUDIOCANAL_PRESENTS_AMAZON_CHANNEL = "Studiocanal Presents Amazon Channel"
    STUDIOCANAL_PRESENTS_APPLE_TV_CHANNEL = "STUDIOCANAL PRESENTS Apple TV Channel"
    SUNDANCE_NOW = "Sundance Now"
    SUNDANCE_NOW_AMAZON_CHANNEL = "Sundance Now Amazon Channel"
    SUNDANCE_NOW_APPLE_TV_CHANNEL = "Sundance Now Apple TV Channel"
    SUPERFRESH_AMAZON_CHANNEL = "Superfresh Amazon Channel"
    SVT = "SVT"
    TELE2_PLAY = "Tele2 Play"
    TELECINE = "Telecine"
    TELECINE_AMAZON_CHANNEL = "Telecine Amazon Channel"
    TELENET = "Telenet"
    TELETOON_PLUS_AMAZON_CHANNEL = "TELETOON+ Amazon Channel"
    TELIA_PLAY = "Telia Play"
    TF1_PLUS = "TF1+"
    TIMVISION = "Timvision"
    TIVIFY = "Tivify"
    TOD = "TOD"
    TOD_TV = "TOD TV"
    TRIART_PLAY = "TriArt Play"
    TV_2 = "TV 2"
    TV_2_PLAY = "TV 2 Play"
    TV_PLUS = "TV+"
    TV2_SKYSHOWTIME = "TV2 Skyshowtime"
    TVING = "TVING"
    TVP = "TVP"
    U_NEXT = "U-NEXT"
    UNIVERSAL_PLUS_AMAZON_CHANNEL = "Universal+ Amazon Channel"
    UNIVERSCINE = "Universcine"
    UPC_TV = "UPC TV"
    USA_NETWORK = "USA Network"
    VERLEIHSHOP = "Verleihshop"
    VI_MOVIES_AND_TV = "VI movies and tv"
    VIAPLAY = "Viaplay"
    VIDDLA = "Viddla"
    VIDEOBUSTER = "Videobuster"
    VIDEOLAND = "Videoland"
    VIDEOLOAD = "Videoload"
    VIDIO = "Vidio"
    VIVA_BY_VIDEOFUTUR = "VIVA by videofutur"
    VIX_GRATIS_AMAZON_CHANNEL = "Vix Gratis Amazon Channel"
    WATCHA = "Watcha"
    WAVVE = "wavve"
    WOW = "WOW"
    WOW_FICTION_AMAZON_CHANNEL = "Wow Fiction Amazon Channel"
    XIVE_TV_DOCUMENTARIES_AMAZON_CHANNEL = "Xive TV Documentaries Amazon Channel"
    YLE_AREENA = "Yle Areena"
    YOUTUBE = "YouTube"
    YOUTUBE_PREMIUM = "YouTube Premium"
    YOUTUBE_TV = "YouTube TV"
    VOYO = "Voyo"
    ZDF = "ZDF"
    ZEE5 = "Zee5"


@dataclass
class Provider:
    canonical_name: str
    names: set[str] = field(default_factory=set)  # observed aliases
    regions: list[dict[str, str]] = field(default_factory=list)  # region code, type (flatrate, rent, buy, ads)

    ALIASES: ClassVar[dict[str, set[str]]] = {
        ProviderName.ABC_IVIEW.value: {"abc iview"},
        ProviderName.ACONTRA_PLUS.value: {"acontra plus", "acontra+"},
        ProviderName.ACONTRA_PLUS_AMAZON_CHANNEL.value: {"acontra plus amazon channel", "acontra+ amazon channel"},
        ProviderName.ACORNTV.value: {"acorntv", "acorn tv"},
        ProviderName.ACORNTV_AMAZON_CHANNEL.value: {"acorntv amazon channel", "acorn tv amazon channel"},
        ProviderName.ACORNTV_APPLE_TV.value: {"acorn tv apple tv", "acorntv apple tv"},
        ProviderName.ACTION_MAX_AMAZON_CHANNEL.value: {"action max amazon channel"},
        ProviderName.ALLENTE.value: {"allente"},
        ProviderName.ALLESKINO.value: {"alleskino"},
        ProviderName.ALLESKINO_AMAZON_CHANNEL.value: {"alleskino amazon channel"},
        ProviderName.AMAZON_PRIME_VIDEO.value: {
            "amazon video",
            "amazon prime video",
            "amazon prime video with ads",
            "amazon prime video free with ads",
        },
        ProviderName.AMC.value: {"amc"},
        ProviderName.AMC_CHANNELS_AMAZON_CHANNEL.value: {"amc channels amazon channel"},
        ProviderName.AMC_PLUS.value: {"amc+"},
        ProviderName.AMC_PLUS_AMAZON_CHANNEL.value: {"amc+ amazon channel", "amc plus amazon channel"},
        ProviderName.AMC_PLUS_APPLE_TV_CHANNEL.value: {"amc plus apple tv channel", "amc+ apple tv channel"},
        ProviderName.AMC_PLUS_ROKU_PREMIUM_CHANNEL.value: {
            "amc+ roku premium channel",
            "amc plus roku premium channel",
        },
        ProviderName.APPLE_TV.value: {"apple tv", "apple tv store"},
        ProviderName.APPLE_TV_PLUS.value: {"apple tv+", "apple tv plus"},
        ProviderName.ARD_PLUS.value: {"ard plus", "ard+"},
        ProviderName.ARD_PLUS_AMAZON_CHANNEL.value: {"ard plus amazon channel"},
        ProviderName.ARD_PLUS_APPLE_TV_CHANNEL.value: {"ard plus apple tv channel", "ard+ apple tv channel"},
        ProviderName.ARTE_BOUTIQUE.value: {"arte boutique"},
        ProviderName.ARTHOUSE_CNMA.value: {"arthouse cnma", "arthousecnma"},
        ProviderName.ARTHOUSE_CNMA_AMAZON_CHANNEL.value: {"arthouse cnma amazon channel"},
        ProviderName.ASIANCRUSH.value: {"asiancrush"},
        ProviderName.ATRES_PLAYER.value: {"atres player"},
        ProviderName.BBC_IPLAYER.value: {"bbc iplayer"},
        ProviderName.BBOX_VOD.value: {"bbox vod", "bbox"},
        ProviderName.BEAMAFILM.value: {"beamafilm"},
        ProviderName.BELAS_ARTES_A_LA_CARTE.value: {"belas artes à la carte", "belas artes a la carte"},
        ProviderName.BE_TV_GO.value: {"be tv go"},
        ProviderName.BFI_PLAYER.value: {"bfi player"},
        ProviderName.BFI_PLAYER_AMAZON_CHANNEL.value: {"bfi player amazon channel"},
        ProviderName.BFI_PLAYER_APPLE_TV_CHANNEL.value: {"bfi player apple tv channel"},
        ProviderName.BINGE.value: {"binge"},
        ProviderName.BLOCKBUSTER.value: {"blockbuster"},
        ProviderName.BLOODY_MOVIES_AMAZON_CHANNEL.value: {"bloody movies amazon channel"},
        ProviderName.BLUE_TV.value: {"blue tv"},
        ProviderName.BROADWAYHD.value: {"broadwayhd"},
        ProviderName.BRITBOX.value: {"britbox", "brit box"},
        ProviderName.BRITBOX_AMAZON_CHANNEL.value: {"britbox amazon channel"},
        ProviderName.BRITBOX_APPLE_TV_CHANNEL.value: {"britbox apple tv channel"},
        ProviderName.CANAL_PLUS.value: {"canal+", "canal plus"},
        ProviderName.CANAL_VOD.value: {"canal vod"},
        ProviderName.CATCHPLAY.value: {"catchplay"},
        ProviderName.CDA_PREMIUM.value: {"cda premium"},
        ProviderName.CG_TV_STREAMING.value: {"cg tv streaming"},
        ProviderName.CHANNEL_4_PLUS.value: {"channel 4 plus", "channel 4+"},
        ProviderName.CHILI.value: {"chili"},
        ProviderName.CINEASTERNA.value: {"cineasterna"},
        ProviderName.CINEMAS_A_LA_DEMANDE.value: {"cinemas a la demande", "cinemas à la demande"},
        ProviderName.CINEMAX_AMAZON_CHANNEL.value: {"cinemax amazon channel"},
        ProviderName.CINEMAX_APPLE_TV_CHANNEL.value: {"cinemax apple tv channel"},
        ProviderName.CINEMEMBER.value: {"cinemember"},
        ProviderName.CINE_PLUS_OCS_AMAZON_CHANNEL.value: {"cine+ ocs amazon channel"},
        ProviderName.CINOBO.value: {"cinobo"},
        ProviderName.CINU.value: {"cinu"},
        ProviderName.CLARO_TV_PLUS.value: {"claro tv+"},
        ProviderName.CLARO_VIDEO.value: {"claro video"},
        ProviderName.CLUB_ILLICO.value: {"club illico"},
        ProviderName.COSMOGO.value: {"cosmogo"},
        ProviderName.CRAVE.value: {"crave"},
        ProviderName.CRAVE_AMAZON_CHANNEL.value: {"crave amazon channel"},
        ProviderName.CRITERION_CHANNEL.value: {"criterion channel"},
        ProviderName.CRUNCHYROLL.value: {"crunchyroll"},
        ProviderName.CRUNCHYROLL_AMAZON_CHANNEL.value: {"crunchyroll amazon channel"},
        ProviderName.CULTPIX.value: {"cultpix"},
        ProviderName.CURIOSITY_STREAM.value: {"curiosity stream", "curiositystream"},
        ProviderName.CURIOSITY_STREAM_AMAZON_CHANNEL.value: {
            "curiosity stream amazon channel",
            "curiositystream amazon channel",
        },
        ProviderName.CURIOSITY_STREAM_APPLE_TV_CHANNEL.value: {
            "curiosity stream apple tv channel",
            "curiositystream apple tv channel",
        },
        ProviderName.CURZON_HOME_CINEMA.value: {"curzon home cinema"},
        ProviderName.CURZON_AMAZON_CHANNEL.value: {"curzon amazon channel"},
        ProviderName.DANIME_AMAZON_CHANNEL.value: {"danime amazon channel"},
        ProviderName.DISCOVERY_PLUS.value: {"discovery +", "discovery+", "discovery plus"},
        ProviderName.DISCOVERY_PLUS_AMAZON_CHANNEL.value: {
            "discovery+ amazon channel",
            "discovery plus amazon channel",
        },
        ProviderName.DISNEY_PLUS.value: {"disney plus", "disney+"},
        ProviderName.DISNEY_PLUS_AMAZON_CHANNEL.value: {"disney+ amazon channel"},
        ProviderName.DOCPLAY.value: {"docplay"},
        ProviderName.DOCPLAY_AMAZON_CHANNEL.value: {"docplay amazon channel"},
        ProviderName.DOCSVILLE.value: {"docsville"},
        ProviderName.DOCURAMAFILMS_AMAZON_CHANNEL.value: {"docuramafilms amazon channel"},
        ProviderName.DRAKEN_FILMS.value: {"draken films"},
        ProviderName.ELISA_VIIHDE.value: {"elisa viihde"},
        ProviderName.ETERNAL_FAMILY.value: {"eternal family"},
        ProviderName.FANDANGO_AT_HOME.value: {"fandango at home", "fandango at home free"},
        ProviderName.FANDOR_AMAZON_CHANNEL.value: {"fandor amazon channel"},
        ProviderName.FAR_EAST_AMAZON_CHANNEL.value: {"far east amazon channel"},
        ProviderName.FAWESOME.value: {"fawesome"},
        ProviderName.FETCH_TV.value: {"fetch tv"},
        ProviderName.FILMBOX_PLUS.value: {"filmbox+", "film box+", "filmbox plus"},
        ProviderName.FILMIN.value: {"filmin", "filmin plus"},
        ProviderName.FILMINGO.value: {"filmingo"},
        ProviderName.FILMO.value: {"filmo"},
        ProviderName.FILMOTEKET.value: {"filmoteket"},
        ProviderName.FILMSTRIBEN.value: {"filmstriben"},
        ProviderName.FLIXFLING.value: {"flixfling"},
        ProviderName.FLIXHOUSE.value: {"flixhouse"},
        ProviderName.FLIXOLE.value: {"flixolé", "flixole"},
        ProviderName.FLIXOLE_AMAZON_CHANNEL.value: {"flixolé amazon channel", "flixole amazon channel"},
        ProviderName.FLIXOLE_APPLE_TV_CHANNEL.value: {"flixolé apple tv channel", "flixole apple tv channel"},
        ProviderName.FOD.value: {"fod"},
        ProviderName.FOD_CHANNEL_AMAZON_CHANNEL.value: {"fod channel amazon channel"},
        ProviderName.FOXTEL_NOW.value: {"foxtel now"},
        ProviderName.FREENET_MEINVOD.value: {"freenet meinvod"},
        ProviderName.FUBOTV.value: {"fubotv"},
        ProviderName.FXNOW.value: {"fxnow"},
        ProviderName.GALACTIC_STREAM_AMAZON_CHANNEL.value: {"galactic stream amazon channel"},
        ProviderName.GLOBOPLAY.value: {"globoplay"},
        ProviderName.GO3.value: {"go3"},
        ProviderName.GOOGLE_PLAY_MOVIES.value: {"google play movies"},
        ProviderName.GUIDEDOC.value: {"guidedoc"},
        ProviderName.HBO_MAX.value: {"hbo max"},
        ProviderName.HBO_MAX_AMAZON_CHANNEL.value: {"hbo max  amazon channel"},
        ProviderName.HBO_MAX_ON_U_NEXT.value: {"hbo max on u-next", "hbo max on u next"},
        ProviderName.HISTORAMA.value: {"historama"},
        ProviderName.HISTORAMA_AMAZON_CHANNEL.value: {"historama amazon channel"},
        ProviderName.HISTORAMA_APPLE_TV_CHANNEL.value: {"historama apple tv channel"},
        ProviderName.HOICHOI.value: {"hoichoi"},
        ProviderName.HOICHOI_AMAZON_CHANNEL.value: {"hoichoi amazon channel"},
        ProviderName.HOICHOI_APPLE_TV_CHANNEL.value: {"hoichoi apple tv channel"},
        ProviderName.HOLLYWOOD_SUITE.value: {"hollywood suite"},
        ProviderName.HOLLYWOOD_SUITE_AMAZON_CHANNEL.value: {"hollywood suite amazon channel"},
        ProviderName.HOME_OF_HORROR.value: {"home of horror"},
        ProviderName.HOME_OF_HORROR_AMAZON_CHANNEL.value: {"home of horror amazon channel"},
        ProviderName.HOOPLA.value: {"hoopla"},
        ProviderName.HOTSTAR.value: {"hotstar"},
        ProviderName.HULU.value: {"hulu"},
        ProviderName.HUNGAMA_PLAY.value: {"hungama play"},
        ProviderName.ICITOUTV.value: {"icitoutv"},
        ProviderName.IFLIX.value: {"iflix"},
        ProviderName.INFINITY_SELECTION_AMAZON_CHANNEL.value: {"infinity selection amazon channel"},
        ProviderName.ITVX_PREMIUM.value: {"itvx premium"},
        ProviderName.IWONDER_FULL_AMAZON_CHANNEL.value: {"iwonder full amazon channel"},
        ProviderName.JIOHOTSTAR.value: {"jiohotstar"},
        ProviderName.JOYN.value: {"joyn"},
        ProviderName.JOYN_PLUS.value: {"joyn plus", "joyn+"},
        ProviderName.JUSTWATCHTV.value: {"justwatchtv", "justwatch tv"},
        ProviderName.KANOPY.value: {"kanopy"},
        ProviderName.KINO_ON_DEMAND.value: {"kino on demand"},
        ProviderName.KINOPOISK.value: {"kinopoisk"},
        ProviderName.KIRJASTOKINO.value: {"kirjastokino"},
        ProviderName.KPN.value: {"kpn"},
        ProviderName.LACINETEK.value: {"lacinetek"},
        ProviderName.LEPSI_TV.value: {"lepsi tv"},
        ProviderName.LINE_TV.value: {"line tv"},
        ProviderName.LIONSGATE_PLAY.value: {"lionsgate play"},
        ProviderName.LIONSGATE_PLAY_AMAZON_CHANNEL.value: {"lionsgate play amazon channel"},
        ProviderName.LIONSGATE_PLAY_APPLE_TV_CHANNEL.value: {"lionsgate play apple tv channel"},
        ProviderName.LIONSGATE_PLUS_AMAZON_CHANNELS.value: {
            "lionsgate+ amazon channels",
            "lionsgate plus amazon channels",
        },
        ProviderName.MAGELLAN_TV.value: {"magellan tv"},
        ProviderName.MAGENTA_TV.value: {"magenta tv"},
        ProviderName.MAGENTA_TV_PLUS.value: {"magenta tv+"},
        ProviderName.MAXDOME_STORE.value: {"maxdome store"},
        ProviderName.MEJANE.value: {"mejane"},
        ProviderName.MERCADO_PLAY.value: {"mercado play"},
        ProviderName.MGM_PLUS.value: {"mgm plus", "mgm+"},
        ProviderName.MGM_PLUS_AMAZON_CHANNEL.value: {"mgm+ amazon channel", "mgm plus amazon channel"},
        ProviderName.MGM_PLUS_ROKU_PREMIUM_CHANNEL.value: {
            "mgm plus roku premium channel",
            "mgm+ roku premium channel",
        },
        ProviderName.MIDNIGHT_FACTORY_AMAZON_CHANNEL.value: {"midnight factory amazon channel"},
        ProviderName.MIDNIGHT_PULP.value: {"midnight pulp"},
        ProviderName.MIDNIGHT_PULP_AMAZON_CHANNEL.value: {"midnight pulp amazon channel"},
        ProviderName.MOLOTOV_TV.value: {"molotov tv"},
        ProviderName.MORE_TV.value: {"more tv"},
        ProviderName.MOVISTARTV.value: {"movistartv"},
        ProviderName.MOVISTAR_PLUS.value: {"movistar plus+", "movistar plus"},
        ProviderName.MOVISTAR_PLUS_FICCION_TOTAL.value: {
            "movistar plus+ ficción total",
            "movistar plus ficcion total",
            "movistar plus+ ficcion total",
        },
        ProviderName.MTV_KATSOMO.value: {"mtv katsomo"},
        ProviderName.MUBI.value: {"mubi"},
        ProviderName.MUBI_AMAZON_CHANNEL.value: {"mubi amazon channel"},
        ProviderName.MYMOVIES_ONE.value: {"mymovies one", "my movies one"},
        ProviderName.NEON_TV.value: {"neon tv"},
        ProviderName.NETFLIX.value: {"netflix", "netflix standard with ads", "netflix kids"},
        ProviderName.NETZKINO.value: {"netzkino"},
        ProviderName.NIGHT_FLIGHT_PLUS.value: {"night flight plus", "night flight+"},
        ProviderName.NOW_TV.value: {"now tv"},
        ProviderName.NOW_TV_CINEMA.value: {"now tv cinema"},
        ProviderName.OKKO.value: {"okko"},
        ProviderName.OLDFLIX.value: {"oldflix"},
        ProviderName.ONEPLAY.value: {"oneplay"},
        ProviderName.ORANGE_VOD.value: {"orange vod"},
        ProviderName.OSN_PLUS.value: {"osn+"},
        ProviderName.OVID.value: {"ovid"},
        ProviderName.OZFLIX.value: {"ozflix"},
        ProviderName.PARAMOUNT_PLUS.value: {
            "paramount plus",
            "paramount plus premium",
            "paramount plus essential",
            "paramount plus basic with ads",
        },
        ProviderName.PARAMOUNT_PLUS_AMAZON_CHANNEL.value: {
            "paramount+ amazon channel",
            "paramount plus amazon channel",
        },
        ProviderName.PARAMOUNT_PLUS_APPLE_TV_CHANNEL.value: {
            "paramount plus apple tv channel",
            "paramount+ apple tv channel",
        },
        ProviderName.PARAMOUNT_PLUS_ROKU_PREMIUM_CHANNEL.value: {"paramount+ roku premium channel"},
        ProviderName.PATHE_HOME.value: {"pathé home", "pathe home"},
        ProviderName.PATHE_THUIS.value: {"pathé thuis", "pathe thuis"},
        ProviderName.PEACOCK.value: {"peacock", "peacock premium", "peacock premium plus"},
        ProviderName.PHILO.value: {"philo"},
        ProviderName.PILOT_WP.value: {"pilot wp"},
        ProviderName.PLAYER.value: {"player"},
        ProviderName.PLEX.value: {"plex"},
        ProviderName.PLEX_CHANNEL.value: {"plex channel"},
        ProviderName.POLSAT_BOX_GO.value: {"polsat box go"},
        ProviderName.PREMIERE_MAX.value: {"premiere max"},
        ProviderName.PREMIERY_CANAL_PLUS.value: {"premiery canal+", "premiery canal plus"},
        ProviderName.PRIMA_PLUS.value: {"prima plus", "prima+"},
        ProviderName.QUEENS_CLUB.value: {"queens club"},
        ProviderName.QUEENS_CLUB_AMAZON_CHANNEL.value: {"queens club amazon channel"},
        ProviderName.RAKUTEN_TV.value: {"rakuten tv"},
        ProviderName.RESERVA_IMOVISION_AMAZON_CHANNEL.value: {"reserva imovision amazon channel"},
        ProviderName.RETROCRUSH.value: {"retrocrush"},
        ProviderName.RETROCRUSH_AMAZON_CHANNEL.value: {"retrocrush amazon channel"},
        ProviderName.REVEEL.value: {"reveel"},
        ProviderName.RTBF_AUVIO.value: {"rtbf auvio"},
        ProviderName.RTL_PLUS.value: {"rtl+", "rtl plus"},
        ProviderName.RTL_PLUS_MAX_AMAZON_CHANNEL.value: {"rtl+ max amazon channel", "rtl plus max amazon channel"},
        ProviderName.RUUTU.value: {"ruutu"},
        ProviderName.SF_ANYTIME.value: {"sf anytime"},
        ProviderName.SHADOWZ.value: {"shadowz"},
        ProviderName.SHADOWZ_AMAZON_CHANNEL.value: {"shadowz amazon channel"},
        ProviderName.SHAHID_VIP.value: {"shahid vip"},
        ProviderName.SHOWMAX.value: {"showmax"},
        ProviderName.SHUDDER.value: {"shudder"},
        ProviderName.SHUDDER_AMAZON_CHANNEL.value: {"shudder amazon channel"},
        ProviderName.SHUDDER_APPLE_TV_CHANNEL.value: {"shudder apple tv channel"},
        ProviderName.SKY.value: {"sky"},
        ProviderName.SKYSHOWTIME.value: {"skyshowtime"},
        ProviderName.SKY_GO.value: {"sky go"},
        ProviderName.SKY_STORE.value: {"sky store"},
        ProviderName.SKY_X.value: {"sky x"},
        ProviderName.SONY_LIV.value: {"sony liv"},
        ProviderName.SONY_ONE_AMAZON_CHANNEL.value: {"sony one amazon channel"},
        ProviderName.SONY_PICTURES_AMAZON_CHANNEL.value: {"sony pictures amazon channel"},
        ProviderName.SOONER.value: {"sooner"},
        ProviderName.SPECTRUM_ON_DEMAND.value: {"spectrum on demand"},
        ProviderName.STAN.value: {"stan"},
        ProviderName.STARZ.value: {"starz"},
        ProviderName.STARZPLAY.value: {"starzplay"},
        ProviderName.STARZ_AMAZON_CHANNEL.value: {"starz amazon channel"},
        ProviderName.STARZ_APPLE_TV_CHANNEL.value: {"starz apple tv channel"},
        ProviderName.STARZ_ROKU_PREMIUM_CHANNEL.value: {"starz roku premium channel"},
        ProviderName.STRIM.value: {"strim"},
        ProviderName.STUDIOCANAL_PRESENTS_AMAZON_CHANNEL.value: {"studiocanal presents amazon channel"},
        ProviderName.STUDIOCANAL_PRESENTS_APPLE_TV_CHANNEL.value: {"studiocanal presents apple tv channel"},
        ProviderName.SUNDANCE_NOW.value: {"sundance now"},
        ProviderName.SUNDANCE_NOW_AMAZON_CHANNEL.value: {"sundance now amazon channel"},
        ProviderName.SUNDANCE_NOW_APPLE_TV_CHANNEL.value: {"sundance now apple tv channel"},
        ProviderName.SUPERFRESH_AMAZON_CHANNEL.value: {"superfresh amazon channel"},
        ProviderName.SVT.value: {"svt"},
        ProviderName.TELE2_PLAY.value: {"tele2 play"},
        ProviderName.TELECINE.value: {"telecine"},
        ProviderName.TELECINE_AMAZON_CHANNEL.value: {"telecine amazon channel"},
        ProviderName.TELENET.value: {"telenet"},
        ProviderName.TELETOON_PLUS_AMAZON_CHANNEL.value: {"teletoon+ amazon channel", "teletoon plus amazon channel"},
        ProviderName.TELIA_PLAY.value: {"telia play"},
        ProviderName.TF1_PLUS.value: {"tf1+", "tf1 plus"},
        ProviderName.TIMVISION.value: {"timvision"},
        ProviderName.TIVIFY.value: {"tivify"},
        ProviderName.TOD.value: {"tod"},
        ProviderName.TOD_TV.value: {"tod tv"},
        ProviderName.TRIART_PLAY.value: {"triart play"},
        ProviderName.TV_2.value: {"tv 2"},
        ProviderName.TV_2_PLAY.value: {"tv 2 play"},
        ProviderName.TV_PLUS.value: {"tv+"},
        ProviderName.TV2_SKYSHOWTIME.value: {"tv2 skyshowtime"},
        ProviderName.TVING.value: {"tving"},
        ProviderName.TVP.value: {"tvp"},
        ProviderName.U_NEXT.value: {"u-next"},
        ProviderName.UNIVERSAL_PLUS_AMAZON_CHANNEL.value: {"universal+ amazon channel"},
        ProviderName.UNIVERSCINE.value: {"universcine"},
        ProviderName.UPC_TV.value: {"upc tv"},
        ProviderName.USA_NETWORK.value: {"usa network"},
        ProviderName.VERLEIHSHOP.value: {"verleihshop"},
        ProviderName.VI_MOVIES_AND_TV.value: {"vi movies and tv"},
        ProviderName.VIAPLAY.value: {"viaplay"},
        ProviderName.VIDDLA.value: {"viddla"},
        ProviderName.VIDEOBUSTER.value: {"videobuster"},
        ProviderName.VIDEOLAND.value: {"videoland"},
        ProviderName.VIDEOLOAD.value: {"videoload"},
        ProviderName.VIDIO.value: {"vidio"},
        ProviderName.VIVA_BY_VIDEOFUTUR.value: {"viva by videofutur"},
        ProviderName.VIX_GRATIS_AMAZON_CHANNEL.value: {"vix gratis amazon channel"},
        ProviderName.WATCHA.value: {"watcha"},
        ProviderName.WAVVE.value: {"wavve"},
        ProviderName.WOW.value: {"wow"},
        ProviderName.WOW_FICTION_AMAZON_CHANNEL.value: {"wow fiction amazon channel"},
        ProviderName.XIVE_TV_DOCUMENTARIES_AMAZON_CHANNEL.value: {"xive tv documentaries amazon channel"},
        ProviderName.YLE_AREENA.value: {"yle areena"},
        ProviderName.YOUTUBE.value: {"youtube"},
        ProviderName.YOUTUBE_PREMIUM.value: {"youtube premium"},
        ProviderName.YOUTUBE_TV.value: {"youtube tv"},
        ProviderName.VOYO.value: {"voyo"},
        ProviderName.ZDF.value: {"zdf"},
        ProviderName.ZEE5.value: {"zee5"},
    }
    # build reverse lookup: maps lowercased alias or canonical -> ProviderName
    REVERSE_LOOKUP: ClassVar[dict[str, ProviderName]] = {}
    for canonical, aliases in ALIASES.items():
        try:
            enum_member = ProviderName(canonical)
        except ValueError:
            # should not happen if ALIASES keys match ProviderName values
            continue
        REVERSE_LOOKUP[canonical.lower()] = enum_member
        for alias in aliases:
            REVERSE_LOOKUP[alias.lower()] = enum_member

    def __post_init__(self):
        """Convert canonical_name to string if it's provided as a ProviderName enum."""
        if isinstance(self.canonical_name, ProviderName):
            self.canonical_name = self.canonical_name.value

    def __repr__(self):
        return f"Provider({self.canonical_name}, regions={self.regions})"

    @staticmethod
    def get_provider_name(name: str) -> ProviderName:
        if not name:
            raise ValueError("name must be provided")
        provider_name = Provider.REVERSE_LOOKUP.get(name.strip().lower())
        if provider_name is None:
            raise ValueError(f"Unknown provider name: {name}")
        return provider_name

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Return the canonical provider name based on aliases (case-insensitive).
        If not found, return the original name.
        """
        if not name:
            return ""
        n = name.lower()
        for canonical, aliases in Provider.ALIASES.items():
            if n in aliases:
                return canonical
        return name  # keep as-is if no alias match


class TMDBMovie:
    def __init__(
        self,
        id: str,
        imdb_id: str | None,
        title: str,
        year: int | None = None,
        original_title: str | None = None,
        alternative_titles: dict[str, str] = None,
        duration: int | None = None,
        original_language: str | None = None,
        spoken_languages: list[str | None] = [],
        origin_countries: list[str] = [],
        genres: list[str | None] = None,
        overview: str | None = None,
        vote_average: float | None = None,
        providers: list[Provider] = [],
    ):
        self.id = id
        self.imdb_id = imdb_id
        self.title = title
        self.year = year
        self.original_title = original_title
        self.alternative_titles = alternative_titles
        self.duration = duration
        self.original_language = original_language
        self.spoken_languages = spoken_languages
        self.origin_countries = origin_countries
        self.genres = genres
        self.overview = overview
        self.vote_average = vote_average
        self.providers = providers

    def __repr__(self):
        return f"TMDBMovie(id={self.id}, title='{self.title}', original_title='{self.original_title}', year={self.year}, duration={self.duration})"

    def get_provider(self, provider_name: ProviderName) -> Provider | None:
        """
        Return the Provider whose canonical_name matches `provider` (case-insensitive).
        If not found or provider is empty, return None.
        """
        if not provider_name:
            return None
        target = provider_name.value.strip().lower()
        for p in self.providers or []:
            if p.canonical_name.lower() == target:
                return p
        return None

    @staticmethod
    def sanitize(text: str, folder: bool = False) -> str:
        """
        Sanitizes a string to be safe for use as a file or folder name on Windows/macOS/Linux.

        Args:
            text (str): The string to sanitize.
            folder (bool): Whether the string is intended to be a folder name or filename. Defaults to False.
        Returns:
            str: The sanitized string, or an empty string if the input was Falsey.
        """
        if not text:
            return ""
        s = re.sub(r'[\x00-\x1f<>:"/\\|?*\x7f\xa0]+', " ", text).strip()  # strip invalid chars for Windows/macOS/Linux
        if folder:
            s = re.sub(r"\s+", " ", s)
            s = re.sub(r"[‐–—⁃]", "-", s)  # replace bad hyphens
        else:
            s = s.replace("…", ".")
            s = re.sub(r"\s+", ".", s)
            s = re.sub(r"\.+", ".", s)
            s = s.strip(".")
            s = re.sub(r"\.(?:-|‐|–|—|⁃)\.", ".", s)  # fix bad hyphen types
            s = s.replace(",.", ".")
        if os.name == "nt":
            s = TMDBMovie.make_windows_safe(s)
        return s.strip() or ""

    @staticmethod
    def make_windows_safe(text: str) -> str:
        """
        Sanitize Windows reserved device names from a string.
        Appends '_' to any reserved Windows device names (CON, PRN, AUX, NUL, COM1-COM9, LPT1-LPT9)
        if they would cause an OSError to be thrown by the filesystem.

        Args:
            text (str): The input string to sanitize.
        Returns:
            str: The sanitized string with reserved names modified to be safe for Windows file names.
        """
        # fmt: off
        reserved_names = {
            "AUX", "CON", "NUL", "PRN",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
        }
        # fmt: on
        # split by dot to check each component
        parts = text.split(".", 1)
        if parts and parts[0].rstrip(" .").upper() in reserved_names:
            parts[0] += "_"
        return ".".join(parts)
