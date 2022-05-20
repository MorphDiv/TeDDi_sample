WALS Chapter Coverage
================
Chris Bentz
05/20/2022

## Load Packages

``` r
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
library(ggplot2)
library(reshape2)
```

## Load Data

Load the data with WALS chapter information as well as language information for languages included in the 100 language sample (in csv format).

``` r
wals.chapters <- read.csv("~/Github/TeDDi_sample/LangInfo/Sources/WALS/WALS_languages_chapters.csv", header = T, na.strings = c("", "NA"))
wals.100 <- read.csv("~/Github/TeDDi_sample/LangInfo/langInfo_TeDDi.csv")
```

Some pre-processing steps.

``` r
# exclude languages for which there is currently no text data
missing = c("krk", "koa", "kse", "lkt", "lez", "myi", "mei", "mar", "sla", "ond", "tuk")
wals.100 <- wals.100[!(wals.100$wals_code %in% missing), ]
# shorten to the relevant columns
wals.100.short <- select(wals.100, wals_code, name_wals)
# order alphabetically
wals.100.short <- wals.100.short[order(wals.100.short$wals_code), ]
# shorten chapter data frame to the relevant columns
wals.chapters.short <- select(wals.chapters, wals_code, X1A.Consonant.Inventories:X79B.Suppletion.in.Imperatives.and.Hortatives)
```

## Merge

Merge the two data frames together by wals code.

``` r
wals.100.chapters <- merge(wals.100.short, wals.chapters.short, by = "wals_code")
```

## Calculate Coverage

Get percentages of coverage (filled cells) for each language in the WALS 100 language sample.

``` r
# calculate percentages
coverage <- 1-rowSums(is.na(wals.100.chapters))/(ncol(wals.100.chapters)-2)
# add to data frame
wals.100.coverage <- cbind(wals.100.short, coverage)
```

## Visualize

Visualize coverage percentages with bar plot.

``` r
# order according to coverage percentages
coverage.plot <- ggplot(data = wals.100.coverage, aes(x = reorder(name_wals, -coverage), y = coverage , fill = coverage)) + 
  geom_bar(stat = "identity") +
  xlab("Language (WALS name)") +
  ylab("Feature Coverage (%)") +
  #ylim(0,1) +
  geom_text(aes(label = round(coverage, 2)), hjust = 1.2, colour = "black", angle = 90) +
  scale_fill_continuous(low = "red", high = "light blue") +
  theme(legend.position = "none", axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))
print(coverage.plot)
```

![](WALSChapterCoverage_files/figure-markdown_github/unnamed-chunk-6-1.png)

Save to file.

``` r
#ggsave("Barplot_WALSCoverage.pdf", coverage.plot, 
#       dpi = 300, scale = 1, width = 15, height = 5, device = cairo_pdf)
```

## Heatmap

Plot heatmap with all wals features and languages, in which empty cells are indicated by colour.

``` r
wals.100.chapters.long <- melt(wals.100.chapters, id.vars = c("wals_code", "name_wals"))
```

    ## Warning: attributes are not identical across measure variables; they will be
    ## dropped

``` r
heatmap <- ggplot(data = wals.100.chapters.long, aes(x = name_wals, y = variable, fill = is.na(value))) +
  geom_tile() +
  theme(axis.text.x = element_text(angle = 90))
print(heatmap)
```

![](WALSChapterCoverage_files/figure-markdown_github/unnamed-chunk-8-1.png)
