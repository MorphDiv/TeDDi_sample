Grapheme TTR in 100LC
================
Steven Moran
24 August, 2020

Load each grapheme orthography profile (OP) from disk, generate TTRs,
and write to a table.

    # Create results data frame
    header <- c("name", "genre_broad", "types", "tokens", "ttr")
    results <- as.data.frame(matrix(,0,length(header)))
    names(results) <- header

    # Loop over the OPs
    fils <- list.files("../graphemes/orthography_profiles", pattern="csv$", full.names = TRUE, recursive = TRUE)

    # For testing, set to just one file:
    # file <- fils[1]

    col_types <- cols(Frequency='i', .default='c')

    for (file in fils) {
      # Get language name from file path
      s <- unlist(strsplit(file, "/"))
      filename <- tail(s, n=1)
      filename <- str_remove(filename, ".csv")
      
      # Read the OP
      df <- read_csv(file, col_types=col_types)

      # Get ttr
      tokens <- sum(df$Frequency)
      types <- length(unique(df$Grapheme))
      ttr <- (types / tokens)
      
      # Recreate the language name and broad genre (this is soooo hacky...)
      genre_broad <- unlist(lapply(str_split(filename, "_"), tail ,n=1))
      fname <- str_remove(filename, paste0("_", genre_broad))
      
      # Add to results data frame
      result <- c(fname, genre_broad, types, tokens, ttr)
      results[nrow(results) + 1,] <- result
    }

    # Clean up
    results$types <- as.integer(results$types)
    results$tokens <- as.integer(results$tokens)
    results$ttr <- as.numeric(results$ttr)

    results %>% kable()

| name                        | genre\_broad | types |   tokens |       ttr |
|:----------------------------|:-------------|------:|---------:|----------:|
| Abkhaz\_abk                 | professional |    64 |    10003 | 0.0063981 |
| Acoma\_kjq                  | non-fiction  |    43 |    15893 | 0.0027056 |
| Alamblak\_amp               | non-fiction  |    66 |  1290455 | 0.0000511 |
| Amele\_aey                  | non-fiction  |    68 |  1160739 | 0.0000586 |
| Apurina\_apu                | non-fiction  |    59 |  1247091 | 0.0000473 |
| Arabic\_Egyptian\_arz       | non-fiction  |   426 |  1961436 | 0.0002172 |
| Arapesh\_Mountain\_ape      | non-fiction  |    69 |  1510912 | 0.0000457 |
| Asmat\_tml                  | conversation |    32 |      870 | 0.0367816 |
| Bagirmi\_bmi                | grammar      |    47 |      210 | 0.2238095 |
| Barasano\_bsn               | non-fiction  |    90 |  1360928 | 0.0000661 |
| Basque\_eus                 | non-fiction  |   172 | 16116015 | 0.0000107 |
| Basque\_eus                 | professional |    54 |     9623 | 0.0056116 |
| Berber\_MiddleAtlas\_tzm    | professional |    70 |     8511 | 0.0082247 |
| Burmese\_mya                | non-fiction  |   663 |  2249570 | 0.0002947 |
| Burmese\_mya                | professional |   273 |     8484 | 0.0321782 |
| Burushaski\_bsk             | grammar      |    40 |      925 | 0.0432432 |
| CanelaKraho\_ram            | non-fiction  |    73 |   192513 | 0.0003792 |
| Chamorro\_cha               | non-fiction  |    76 |   921354 | 0.0000825 |
| Chamorro\_cha               | professional |    61 |     9910 | 0.0061554 |
| Chukchi\_ckt                | non-fiction  |    79 |   134477 | 0.0005875 |
| Daga\_dgz                   | non-fiction  |    64 |   997386 | 0.0000642 |
| Dani\_LowerGrandValley\_dni | conversation |    33 |     1789 | 0.0184461 |
| English\_eng                | fiction      |   289 | 23630990 | 0.0000122 |
| English\_eng                | non-fiction  |   174 | 25054918 | 0.0000069 |
| English\_eng                | professional |    56 |     8891 | 0.0062985 |
| Fijian\_fij                 | non-fiction  |    59 |   861344 | 0.0000685 |
| Fijian\_fij                 | professional |    56 |     9094 | 0.0061579 |
| Finnish\_fin                | fiction      |   171 | 33106295 | 0.0000052 |
| Finnish\_fin                | non-fiction  |   163 | 35407637 | 0.0000046 |
| Finnish\_fin                | professional |    56 |    10835 | 0.0051684 |
| French\_fra                 | fiction      |   247 | 23767792 | 0.0000104 |
| French\_fra                 | non-fiction  |   191 | 25150294 | 0.0000076 |
| French\_fra                 | professional |    60 |     9953 | 0.0060283 |
| Georgian\_kat               | non-fiction  |   173 |  3914602 | 0.0000442 |
| Georgian\_kat               | professional |    46 |    10455 | 0.0043998 |
| German\_deu                 | fiction      |   351 | 27780867 | 0.0000126 |
| German\_deu                 | non-fiction  |   184 | 28779152 | 0.0000064 |
| German\_deu                 | professional |    70 |    10295 | 0.0067994 |
| Gooniyandi\_gni             | conversation |    20 |      775 | 0.0258065 |
| Greek\_Modern\_ell          | fiction      |   358 | 25932449 | 0.0000138 |
| Greek\_Modern\_ell          | non-fiction  |   242 | 28844378 | 0.0000084 |
| Greek\_Modern\_ell          | professional |   118 |    21056 | 0.0056041 |
| Greenlandic\_West\_kal      | non-fiction  |    71 |   726470 | 0.0000977 |
| Greenlandic\_West\_kal      | professional |    50 |    15779 | 0.0031688 |
| Guarani\_gug                | non-fiction  |    94 |   813314 | 0.0001156 |
| Guarani\_gug                | professional |    75 |     7882 | 0.0095154 |
| Hausa\_hau                  | non-fiction  |    71 |   736578 | 0.0000964 |
| Hausa\_hau                  | professional |    61 |    23404 | 0.0026064 |
| Hebrew\_Modern\_heb         | fiction      |   358 |   488629 | 0.0007327 |
| Hebrew\_Modern\_heb         | non-fiction  |   392 | 21215980 | 0.0000185 |
| Hebrew\_Modern\_heb         | professional |    31 |     5983 | 0.0051813 |
| Hindi\_hin                  | non-fiction  |  1081 |  6540546 | 0.0001653 |
| Hindi\_hin                  | professional |   277 |     5821 | 0.0475863 |
| Hixkaryana\_hix             | non-fiction  |    49 |   247518 | 0.0001980 |
| HmongNjua\_hnj              | professional |    57 |    10880 | 0.0052390 |
| Imonda\_imn                 | non-fiction  |    25 |     1599 | 0.0156348 |
| Indonesian\_ind             | non-fiction  |   265 | 32402441 | 0.0000082 |
| Indonesian\_ind             | professional |    52 |    10865 | 0.0047860 |
| Jakaltek\_jac               | non-fiction  |    68 |  1154758 | 0.0000589 |
| Japanese\_jpn               | fiction      |  4349 |  1626514 | 0.0026738 |
| Japanese\_jpn               | non-fiction  |  3843 |  9365709 | 0.0004103 |
| Japanese\_jpn               | professional |   505 |     4091 | 0.1234417 |
| Kannada\_kan                | professional |   287 |     5862 | 0.0489594 |
| Kayardild\_gyd              | grammar      |    21 |      221 | 0.0950226 |
| Kewa\_kew                   | non-fiction  |    64 |  1255293 | 0.0000510 |
| Khalkha\_khk                | non-fiction  |    59 |   783108 | 0.0000753 |
| Khalkha\_khk                | professional |    54 |     9290 | 0.0058127 |
| Khoekhoe\_naq               | non-fiction  |    74 |   718250 | 0.0001030 |
| Kiowa\_kio                  | non-fiction  |    42 |      581 | 0.0722892 |
| Korean\_kor                 | non-fiction  |  2772 | 10433726 | 0.0002657 |
| Korean\_kor                 | professional |   315 |     3531 | 0.0892099 |
| Kutenai\_kut                | non-fiction  |    28 |      278 | 0.1007194 |
| Lango\_laj                  | non-fiction  |    60 |   681594 | 0.0000880 |
| Lavukaleve\_lvk             | non-fiction  |    46 |     7575 | 0.0060726 |
| Luvale\_lue                 | professional |    52 |     8892 | 0.0058480 |
| Makah\_myh                  | conversation |    38 |     1378 | 0.0275762 |
| Makah\_myh                  | non-fiction  |    27 |      233 | 0.1158798 |
| Malagasy\_plt               | non-fiction  |    84 |  3738533 | 0.0000225 |
| Malagasy\_plt               | professional |    58 |    10681 | 0.0054302 |
| Mandarin\_cmn               | fiction      |  9453 |  7395033 | 0.0012783 |
| Mandarin\_cmn               | non-fiction  |  8659 |  9142941 | 0.0009471 |
| Mandarin\_cmn               | professional |   696 |     5592 | 0.1244635 |
| Mapudungun\_arn             | non-fiction  |    66 |  1067903 | 0.0000618 |
| Mapudungun\_arn             | professional |    67 |    12523 | 0.0053502 |
| Martuthunira\_vma           | conversation |    34 |    29771 | 0.0011421 |
| Maung\_mph                  | non-fiction  |    66 |   135696 | 0.0004864 |
| Maybrat\_ayz                | non-fiction  |    32 |     2385 | 0.0134172 |
| Mixtec\_Chalcatongo\_mig    | non-fiction  |    76 |   877602 | 0.0000866 |
| Ngiyambaa\_wyb              | conversation |    19 |      161 | 0.1180124 |
| Oromo\_Harar\_hae           | non-fiction  |    66 |  1000842 | 0.0000659 |
| Otomi\_Mezquital\_ote       | grammar      |     0 |        0 |       NaN |
| Otomi\_Mezquital\_ote       | non-fiction  |     0 |        0 |       NaN |
| Otomi\_Mezquital\_ote       | professional |    72 |     6157 | 0.0116940 |
| Persian\_pes                | fiction      |   200 |    88721 | 0.0022543 |
| Persian\_pes                | non-fiction  |   642 | 21015634 | 0.0000305 |
| Persian\_pes                | professional |    49 |     7146 | 0.0068570 |
| Piraha\_myp                 | non-fiction  |    33 |    22722 | 0.0014523 |
| Quechua\_Imbabura\_qvi      | non-fiction  |    72 |  1226343 | 0.0000587 |
| Rama\_rma                   | grammar      |    28 |     2595 | 0.0107900 |
| Rama\_rma                   | non-fiction  |    23 |     1062 | 0.0216573 |
| Rapanui\_rap                | non-fiction  |    43 |     7924 | 0.0054266 |
| Russian\_rus                | fiction      |   150 |   267516 | 0.0005607 |
| Russian\_rus                | non-fiction  |   232 | 28327840 | 0.0000082 |
| Russian\_rus                | professional |    66 |    10204 | 0.0064681 |
| Sango\_sag                  | non-fiction  |    78 |   920017 | 0.0000848 |
| Sango\_sag                  | professional |    69 |     8196 | 0.0084187 |
| Sanuma\_xsu                 | non-fiction  |    85 |  1511667 | 0.0000562 |
| Spanish\_spa                | fiction      |   200 | 24083125 | 0.0000083 |
| Spanish\_spa                | non-fiction  |   176 | 27079157 | 0.0000065 |
| Spanish\_spa                | professional |    60 |    10038 | 0.0059773 |
| Swahili\_swh                | non-fiction  |    82 |   725026 | 0.0001131 |
| Swahili\_swh                | professional |    62 |     8670 | 0.0071511 |
| Tagalog\_tgl                | fiction      |   154 |  4833124 | 0.0000319 |
| Tagalog\_tgl                | non-fiction  |    83 |  4355512 | 0.0000191 |
| Tagalog\_tgl                | professional |    56 |    11363 | 0.0049283 |
| Thai\_tha                   | non-fiction  |  2003 | 18366621 | 0.0001091 |
| Thai\_tha                   | professional |   262 |     7111 | 0.0368443 |
| Turkish\_tur                | non-fiction  |   180 | 33994537 | 0.0000053 |
| Turkish\_tur                | professional |    56 |     8915 | 0.0062815 |
| Vietnamese\_vie             | non-fiction  |   371 | 20189329 | 0.0000184 |
| Vietnamese\_vie             | professional |   665 |    11291 | 0.0588965 |
| Warao\_wba                  | non-fiction  |    22 |     2183 | 0.0100779 |
| Wichi\_mzh                  | non-fiction  |    92 |  3918965 | 0.0000235 |
| Wichita\_wic                | conversation |    20 |     5552 | 0.0036023 |
| Yagua\_yad                  | non-fiction  |    77 |  1117898 | 0.0000689 |
| Yagua\_yad                  | professional |    64 |     9602 | 0.0066653 |
| Yaqui\_yaq                  | non-fiction  |    51 |  1386107 | 0.0000368 |
| Yoruba\_yor                 | non-fiction  |    98 |  2727263 | 0.0000359 |
| Yoruba\_yor                 | professional |    73 |     9093 | 0.0080282 |
| Zoque\_Copainala\_zoc       | non-fiction  |    36 |     5250 | 0.0068571 |
| Zulu\_zul                   | professional |    60 |     9192 | 0.0065274 |

Write the results to CSV.

    write_csv(results, 'grapheme_ttr.csv')
