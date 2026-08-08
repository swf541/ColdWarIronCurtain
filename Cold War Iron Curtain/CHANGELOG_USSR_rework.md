# USSR State Rework

Full rebuild of the Soviet map from the `provinces.pdn` planning layer, plus 1949-correct
naming, a victory point pass, releasable-nation support and debug break-up tooling.

**States: 2067 → 2101 (+34). Strategic regions: 327 → 329.** All IDs contiguous 1–2101, no gaps, no duplicates.

---

## Map & States

- **Rebuilt the Soviet Union from the `provinces.pdn` state-planning layer.** 172 old SOV
  states replaced by **204** generated ones covering 2,576 land provinces. Province-to-state
  assignment done by majority pixel vote against `definition.csv`; 2,577 of 2,576 provinces
  resolved to a single state unambiguously.
- Colours reused on spatially separate blobs were split into distinct states (one state was
  spanning both the Kuril Islands and Azerbaijan). Five stray 1–77px marks ignored.
- **168 states kept their existing ID**; 36 received new IDs. Four fully-absorbed states
  (Syunik, Mangystau, Balti, Koryakia) were removed and their IDs reused so the ID sequence
  stays contiguous — HOI4 logs `Missing State ID` otherwise.
- **Two new Caucasus states**: `2100 Kuba` (Lezgistan) and `2101 Khunzakh` (Avaristan).
- Province `12434` transferred to `587 Lenkoran` (the Mughan plain).

## Population

- **1950 manpower preserved exactly**: 180,898,954 across the reworked area, against a real
  USSR 1950 figure of 178,547,000. Existing values were already a 1950 model, so they were
  redistributed rather than replaced.
- Redistribution weights urban population properly instead of averaging by area. Calibrating
  the mod's victory point values against the 1959 Soviet census gives ~**63,000 people per VP
  point**; the remainder is spread by terrain habitability.
- Resources (steel, oil, aluminium, chromium, tungsten) reconcile exactly to their pre-rework
  totals.

## Naming — Soviet era, 1949

- **All 204 Soviet states renamed** to their 1949 administrative form (194 changed).
  Full oblast form, native Russian, with local forms Russified as well.
- Historically corrected: Perm → **Molotovskaya Oblast**, Orenburg → **Chkalovskaya Oblast**,
  Kareliya → **Karelo-Finskaya SSR** (a union republic until 1956), Ivano-Frankivsk →
  **Stanislavskaya Oblast**, Khmelnytskyi → **Kamenets-Podolskaya Oblast**.
- Units abolished in 1943–44 reflected: Chechnya → **Groznenskaya Oblast**, Kabardino-Balkaria
  → **Kabardinskaya ASSR**, Karachay-Cherkessia → **Cherkesskaya AO**, Kalmykia → **Stepnoy**.
- Baltics and Caucasus Russified: Tallin, Tartu, Narva, Riga, Liepaya, Yelgava, Daugavpils,
  Kaunas, Vilnyus, Klaypeda, Abkhazskaya ASSR, Adzharskaya ASSR, Ganja → **Kirovabad**.
- Localisation written **in place** to `state_names_l_*.yml` (english, french, japanese,
  russian). No new localisation files.

## Victory Points

- **211 → 294** in the reworked area. All originals kept, **83 added** for 1949 cities that
  had none, and every VP now has a name.
- Positions verified against real city coordinates. The map is a **Miller projection**,
  fitted to ~2px mean error at 15.408 px per degree of longitude.
- 1949 corrections: Novokuznetsk → **Stalinsk**, Mariupol → **Zhdanov**, Vladikavkaz →
  **Dzaudzhikau**, Ganja → **Kirovabad**, Rybinsk → **Shcherbakov**, Lviv → **Lvov**,
  Krivoi Rih → **Krivoy Rog**.
- Fixed a misplaced `Akmolinsk` VP sitting 33px from the actual city.

## Strategic Regions

- Region province lists rewritten so **no state straddles a region boundary** (54 provinces
  moved across 23 files). Every province belongs to exactly one region.

## Releasable Nations

- **30 new country tags** with tag entry, country file, colour, localisation (into the
  existing `countries_l_english.yml`) and a history file:
  - **ASSRs** — Buryat-Mongol `BUR`, Dagestan `DAG`, Kabardinian `KAB`, North Ossetian `NOS`,
    Udmurt `UDM`, Yakut `YAK`, Crimean `CRI`, Adjar `ADJ`, Nakhichevan `NAK`, Karakalpak `KKP`
  - **Autonomous oblasts** — Adygei `ADY`, Gorno-Altai `ALT`, Jewish `JEW`, Khakass `KHK`,
    Cherkess `CHR`, Gorno-Badakhshan `BDK`
  - **National okrugs** — Nenets `NEN`, Khanty-Mansi `HMA`, Yamalo-Nenets `YAM`, Taymyr `TAY`,
    Evenki `EVE`, Ust-Orda Buryat `UOB`, Aga Buryat `AGA`, Chukotka `CKT`, Koryak `KRY`
  - **Caucasus** — Ingush `ING`, Talysh-Mughan `TLM`, Javakhk `JAV`, Avaristan `AVR`,
    Lezgistan `LEZ`
- **Cores added where they were missing**: `RUS` now cores all 103 RSFSR states (it had none),
  and the seven existing ASSR tags (`TTR BSK KOM CHV MRD MRI KLY`) now core their own republics.
- `NGK` (Artsakh) additionally cores `560 Shusha`.
- **63 tags are now releasable**, each verified to hold at least one SOV-owned core.

## Debug Tooling

New `USSR Debug — Break-up Scenarios` decision category (hidden behind a toggle in
`debug_decisions`, `ai_will_do = 0` throughout, free and repeatable):

| scenario | effect |
|---|---|
| Historical Dissolution (1991) | the fifteen union republics |
| Total Breakdown | 56 nations — republics, ASSRs, AOs, okrugs, separatists |
| Autonomous Republics Secede | every ASSR and AO, Union survives |
| National Okrugs Secede | the nine national okrugs |
| Separatist Uprising | Baltics + breakaway regions |
| German ASSR — Volga / North Kazakhstan | two mutually exclusive placements |
| Korean ASSR — Balkhash / Pavlodar | two mutually exclusive placements |
| Restore the Union | annex everything back, reset flags |

---

## Strategic Regions — Central Asia

Kazakhstan (249 provinces) and Turkestan (104) were the two largest regions in the mod.
Split east/west, balanced by province count since that drives supply-area size:

| id | region | provinces | states |
|---|---|---|---|
| 136 | Western Kazakhstan | 130 | 5 |
| 328 | Eastern Kazakhstan | 119 | 13 |
| 251 | Transcaspia | 55 | 9 |
| 329 | Transoxiana | 49 | 9 |

New regions inherit their parent's weather blocks. Localisation into the existing
`strategic_region_names_l_english.yml`.

## Resources — rebuilt on real 1949–50 geology

**The resource codes in this mod do not mean what they say.** Before editing anything here,
read the in-game descriptions:

| code | actually represents | includes |
|---|---|---|
| `oil` | **Petrochemicals** | oil, **coal**, gas, biofuels |
| `steel` | **Construction Metals** | iron/steel, copper, lead, tungsten, molybdenum, manganese |
| `aluminium` | **Light Metals** | bauxite, **chromite**, nickel, zinc, tin, silver, magnesium |
| `tungsten` | **Rare Earths** | REE, **gold**, lithium, palladium |
| `chromium` | **Nuclear Materials** | uranium, plutonium, thorium |
| `rubber` | **Food** | grains, meat, fish, dairy |

Soviet totals were re-based on the USSR's real share of 1949–50 world production, then placed
geologically. Previous placement appeared close to random — Moskovskaya Oblast was the top
steel producer, Yakutia held 83 oil, and Nuclear Materials sat in Orel and Tambov.

| category | before | after | share of world |
|---|---|---|---|
| Petrochemicals | 576 | **671** | 13.2% |
| Construction Metals | 822 | **1143** | 14.4% |
| Light Metals | 371 | **452** | 10.8% |
| Rare Earths | 115 | **462** | 17.4% |
| Nuclear Materials | 158 | **203** | 14.5% |

Anchors: Soviet steel ~28 Mt (~15% of world), coal ~261 Mt (~18%), oil ~38 Mt (~7%),
gold ~100 t (~13%), manganese roughly half the world total, and Dalstroy alone about 45%
of Soviet gold.

Placement highlights:

- **Petrochemicals** — Baku 150, then the Donbass and Kuzbass coalfields, Karaganda, Vorkuta,
  the Volga-Urals "Second Baku", Emba, Grozny, Sakhalin.
- **Construction Metals** — Krivoy Rog 180, Magnitogorsk 140, Donbass 130, Nizhny Tagil 120,
  plus Chiatura manganese at Kutaisi and Dzhezkazgan copper at Karaganda.
- **Light Metals** — Khromtau chromite at Aktyubinsk 90, Norilsk and Monchegorsk nickel,
  North Urals and Tikhvin bauxite.
- **Rare Earths** — Kolyma 140 (Dalstroy gold), Norilsk palladium 100, Aldan 80,
  Lovozero on the Kola Peninsula 45.
- **Nuclear Materials** — Taboshar at Leninabad 70 (Combine No. 6, the ore behind the 1949
  bomb), Zheltye Vody at Krivoy Rog 45, Mailuu-Suu 40, Sillamäe 25.

40 states hold resources; 90 states had spurious ones removed. Soviet occupation zones
(Austria, Port Arthur, Porkkala) were deliberately left untouched.

**Note:** `coal` is defined in `common/resources` but used by no state in the mod — coal is
folded into Petrochemicals instead.

## Bug fixes

- **`map/buildings.txt` state tags.** Every building line is tagged with its state ID; moving
  provinces invalidated 2,267 of them, causing HOI4 to discard buildings including **supply
  nodes**. Retagged by resolving map coordinates against `provinces.bmp` (the method the game
  itself uses). Mismatches inside the reworked area: **290 → 0**. Untouched elsewhere.
- **`colors.txt` was silently disabled.** The file must begin with the literal directive
  `#reload countrycolors`; a UTF-8 BOM in front of it broke parsing and reset **all** country
  colours. BOM removed.
- **Eight tags had `capital = 1254` — Südbaden, in Germany.** A copy-paste placeholder
  affecting `TTR BSK KOM CHV MRD MRI KLY` and **`RUS`**. Repointed to their own core states.
- **Belarus had `capital = 206` — Juznomoravlje, in Moravia.** Now `204 Minskaya Oblast`.
- Redirected references to the four deleted states across `events/Romania.txt`,
  two faction-goal files and `00_Russia_Electoral_Regions.txt`.
- Reattached an orphaned lake province (`16186`) that belonged to two states in the original.
- Mod-wide foreign victory point references reduced from 589 to 462.

## Notes for contributors

- **Cultures** are a positional array, not percentages: `add_to_array = { culture = N }`,
  slot 0 = majority, slots 1–3 = minorities largest-first. IDs are defined in
  `common/scripted_localisation/IC_Cultures.txt` across seven repeated blocks.
  **546 cultures defined, IDs 1–546, no gaps — next free ID is 547.**
  Lezgin, Tabasaran, Nogai, Rutul, Agul, Tsakhur, Kabardian and Balkar are **not yet defined**.
- 102 of the Soviet states are still Russian-majority, including Dagestanskaya ASSR,
  Groznenskaya Oblast, Cherkesskaya AO and Nazran — all of which were solidly non-Russian
  in 1949. Cultural layout is the obvious next pass.
- `AVR` and `LEZ` hold one state each; expand their cores as more states are drawn.
