Words vs graphemes TTR in 100LC
================
Steven Moran
24 August, 2020

    words.ttr <- read_csv('word_ttr.csv')
    words.ttr <- tidyr::unite(words.ttr, name, c(name, genre_broad))
    w.cut <- words.ttr %>% select(name, ttr) %>% rename(word_ttr=ttr)

    graphemes.ttr <- read.csv('grapheme_ttr.csv')
    graphemes.ttr <- tidyr::unite(graphemes.ttr, name, c(name, genre_broad))
    g.cut <- graphemes.ttr %>% select(name, ttr) %>% rename(grapheme_ttr=ttr)

    ttr <- left_join(w.cut, g.cut)

    ## Joining, by = "name"

    library(ggplot2)
    library(ggrepel)
    ggplot(ttr, aes(x=grapheme_ttr, y=word_ttr, label=name)) + 
      geom_point() +
      geom_label_repel(aes(label = name),
                      box.padding   = 0.35, 
                      point.padding = 0.5,
                      segment.color = 'grey50')

![](words_vs_graphemes_ttr_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->
