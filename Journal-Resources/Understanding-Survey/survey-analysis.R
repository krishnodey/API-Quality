########################################################################
# Experiment Results
########################################################################

# delete current environment variables --------
rm(list = ls(all.names = TRUE))
# install and load required packages -------
# (taken from https://stackoverflow.com/questions/4090169/elegant-way-to-check-for-missing-packages-and-install-them)

packageList <- c(
  "Hmisc", "dplyr", "ggplot2", "tidyr", "corrplot", "likert", "effectsize", "scales", "lmtest"
)
newPackages <- packageList[!(packageList %in% installed.packages()[, "Package"])]
if (length(newPackages)) install.packages(newPackages)

for (p in packageList) {
  library(p, character.only = TRUE)
}


# helper function to visually and statistically check the distribution of a data set
checkDataDistribution <- function(data, xaxis.title) {
  hist(data, xlab = xaxis.title)
  # Shapiro-Wilk test for non-normal distribution
  # Null hypothesis with Shapiro-Wilk test is that "data" came from a normally distributed population,
  # i.e. p-value <= 0.05 --> "data" is not normally distributed
  shapiro.test(data)
}
# helper function to calculate the Timed Actual Understandability (TAU)
calculateTAU <- function(effectiveness, efficiency, maxEfficiency) {
  effectiveness * (1 - (efficiency / maxEfficiency))
}


# read data ------------
data <- read.csv("results-survey.csv", na.strings = c("", "NA"), fileEncoding = "UTF-8-BOM")

print(data)

# demographic data
# distribution of professions
data %>%
  select(Profession) %>%
  table()
# distribution of developer perspective
data %>%
  select(DeveloperPerspective) %>%
  table()
# distribution of country
data %>%
  select(Country) %>%
  table()
# distribution of groups
#data %>%
#  select(group_id) %>%
#  table()

# median participant stats by task order group
data %>%
  #group_by(group_id) %>%
  summarise(
    numParticipants = n(),
    medianYearsOfExperience = median(YearsOfExperience, na.rm = TRUE),
    numKnowledgeOfRichardsonMaturityModel = sum(RichardsonMaturity, na.rm = TRUE),
    medianRichardsonMaturityRating = median(MaturityLevel, na.rm = TRUE),
    numDeveloper = sum(is_Developer),
    numStudents = sum(is_Student),
    numAcademia = sum(is_Academia),
    numIndustry = n() - numStudents - numAcademia,
    numCanada = sum(is_Canada)
  )

# variable names for the antipatterns
antipatterns <- c(
  "Amorphous", "Contextless", "CRUDy",
  "Inconsistent", "NonDescriptive", "NonHierarchical",
  "NonPertinent", "NonStandard", "Pluralized",
  "Unversioned", "Tunneling", "InconArchetype", "Ambiguity", "Flat"
)
# variable names for the patterns
patterns <- c(
  "Tidy", "Contextual", "Verbless",
  "Consistent", "Descriptive", "Hierarchical",
  "Pertinent", "Standard", "Singularized",
  "Versioned", "Adherence", "ConArchetype", "Annotation", "Structured"
)


# calculate TAU for every questions
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varPattern <- as.name(p)
  varPatternTime <- as.name(paste(p, "Time", sep = ""))
  varAntipattern <- as.name(ap)
  varAntipatternTime <- as.name(paste(ap, "Time", sep = ""))
  data <- data %>%
    mutate("TAU_{{varPattern}}" := calculateTAU({{ varPattern }}, {{ varPatternTime }}, max({{ varPatternTime }}, {{ varAntipatternTime }}, na.rm = TRUE))) %>%
    mutate("TAU_{{varAntipattern}}" := calculateTAU({{ varAntipattern }}, {{ varAntipatternTime }}, max({{ varPatternTime }}, {{ varAntipatternTime }}, na.rm = TRUE)))
}

print(data)


# --> data now has attributes TAU_<Pattern> and TAU_<Antipattern>

# create custom data frame with understandability ratings and TAU for all rules combined
combinedUndDf <- data.frame(matrix(ncol = 4, nrow = 0))
colnames(combinedUndDf) <- c("Pattern_rating_Und", "Pattern_TAU", "Antipattern_rating_Und", "Antipattern_TAU")
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  
  varRatingPattern <- paste(p, "URating", sep = "")
  varRatingAntipattern <- paste(ap, "URating", sep = "")
  varTAUPattern <- paste("TAU", p, sep = "_")
  varTAUAntipattern <- paste("TAU", ap, sep = "_")
  #print(varRatingAntipattern)
  #print(varTAUPattern)
  
  # merge data frames
  combinedUndDf <- rbind(combinedUndDf, data.frame(
    Pattern_rating = data[[varRatingPattern]],
    Pattern_TAU = data[[varTAUPattern]],
    Antipattern_rating = data[[varRatingAntipattern]],
    Antipattern_TAU = data[[varTAUAntipattern]]
  ))
  
}
print(combinedUndDf)

# Shapiro-Wilk test for non-normal distribution of understandability (replace value with the different rule identifiers, i.e., 1 to 12)
p <- patterns[1]
ap <- antipatterns[1]
varP <- as.name(paste("TAU", p, sep = "_"))
print(varP)
varAP <- as.name(paste("TAU", ap, sep = "_"))
print(varAP)
checkDataDistribution(data[[varP]], varP)
checkDataDistribution(data[[varAP]], varAP)




# create custom data frame with readability ratings and TAU for all rules combined
combinedReadDf <- data.frame(matrix(ncol = 4, nrow = 0))
colnames(combinedReadDf) <- c("Pattern_rating_Read", "Pattern_TAU", "Antipattern_rating_Read", "Antipattern_TAU")
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  
  varRatingPattern <- paste(p, "RRating", sep = "")
  varRatingAntipattern <- paste(ap, "RRating", sep = "")
  varTAUPattern <- paste("TAU", p, sep = "_")
  varTAUAntipattern <- paste("TAU", ap, sep = "_")
 
  
  # merge data frames
  combinedReadDf <- rbind(combinedReadDf, data.frame(
    Pattern_rating = data[[varRatingPattern]],
    Pattern_TAU = data[[varTAUPattern]],
    Antipattern_rating = data[[varRatingAntipattern]],
    Antipattern_TAU = data[[varTAUAntipattern]]
  ))
  
}
print(combinedReadDf)




####################################################################################################
# Calculations for RQ1 (Which design rules have an impact on the understandability of RESTful APIs?)
####################################################################################################

# descriptive statistics

# calculate summary stats for all important performance metrics per individual rule
descriptiveStats <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]

  varTAUP <- as.name(paste("TAU", p, sep = "_"))
  varTAUAP <- as.name(paste("TAU", ap, sep = "_"))
  varP <- as.name(paste(p, "", sep = ""))
  varPTime <- as.name(paste(p, "Time", sep = ""))
  varAP <- as.name(paste(ap, "", sep = ""))
  varAPTime <- as.name(paste(ap, "Time", sep = ""))

  descriptiveStats <- rbind(
    descriptiveStats,
    data %>% summarise(
      rule = p,
      mean_TAU_P := mean({{ varTAUP }}, na.rm = TRUE),
      mean_TAU_AP := mean({{ varTAUAP }}, na.rm = TRUE),
      mean_time_P := mean({{ varPTime }}, na.rm = TRUE),
      mean_time_AP := mean({{ varAPTime }}, na.rm = TRUE),
      correctAnswers_P := sum({{ varP }}, na.rm = TRUE),
      correctAnswers_AP := sum({{ varAP }}, na.rm = TRUE),
      answers_P := data %>% filter(!is.na({{ varP }})) %>% nrow(),
      answers_AP := data %>% filter(!is.na({{ varAP }})) %>% nrow(),
      correctPercent_P := scales::percent(sum({{ varP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varP }})) %>% nrow())),
      correctPercent_AP := scales::percent(sum({{ varAP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varAP }})) %>% nrow())),
      correctness_P := sum({{ varP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varP }})) %>% nrow()),
      correctness_AP := sum({{ varAP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varAP }})) %>% nrow())
    )
  )

}

print(descriptiveStats)

# calculate more detailed descriptive stats per individual rule (min, max, var)
descriptiveStatsDetails <- data.frame()


for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  
  varTAUP <- as.name(paste("TAU", p, sep = "_"))
  varTAUAP <- as.name(paste("TAU", ap, sep = "_"))
  varP <- as.name(paste(p, "", sep = ""))
  varPTime <- as.name(paste(p, "Time", sep = ""))
  varAP <- as.name(paste(ap, "", sep = ""))
  varAPTime <- as.name(paste(ap, "Time", sep = ""))
  

  descriptiveStatsDetails <- rbind(
    descriptiveStatsDetails,
    data %>% summarise(
      rule = p,
      min_TAU_P := min({{ varTAUP }}, na.rm = TRUE),
      min_TAU_AP := min({{ varTAUAP }}, na.rm = TRUE),
      max_TAU_P := max({{ varTAUP }}, na.rm = TRUE),
      max_TAU_AP := max({{ varTAUAP }}, na.rm = TRUE),
      var_TAU_AP := var({{ varTAUP }}, na.rm = TRUE),
      var_TAU_AP := var({{ varTAUAP }}, na.rm = TRUE),
      min_time_AP := min({{ varPTime }}, na.rm = TRUE),
      min_time_AP := min({{ varAPTime }}, na.rm = TRUE),
      max_time_P := max({{ varPTime }}, na.rm = TRUE),
      max_time_AP := max({{ varAPTime }}, na.rm = TRUE),
      var_time_P := var({{ varPTime }}, na.rm = TRUE),
      var_time_AP := var({{ varAPTime }}, na.rm = TRUE)
    )
  )
}

print(descriptiveStatsDetails)

# create a bar plot to easily compare correctPercent
barplotData <- rbind(
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$correctness_P,
    treatment = "pattern"
  ),
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$correctness_AP,
    treatment = "antipattern"
  )
) %>% arrange(factor(rule, levels = rev(p))) %>%
  mutate(index = row_number())

# use ggplot to print the grouped bar chart
ggplot(barplotData, aes(x = reorder(rule, index), y = value, fill = treatment)) +
geom_bar(
  stat = "identity",
  width = 0.5,
  position = position_dodge(0.6)
) +
# colors for "rule" and "violation"
scale_fill_manual(values = c("#dd1100", "#0077dd")) +
# use percent for the scale and control space for the labels
scale_y_continuous(labels = scales::percent, expand = expansion(mult = c(0, .1))) +
# bar label text and positioning
geom_text(
  aes(label = scales::percent(round(value, 2))),
  position = position_dodge(0.6),
  fontface = "bold",
  size = 5,
  hjust = -0.05
) +
theme_classic() +
labs(x = "Rule", y = "Correct answers", fill = "") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 16),
  axis.text.x = element_text(size = 14),
  axis.text.y = element_text(size = 14),
  legend.title = element_text(size = 16),
  legend.text = element_text(size = 16),
  legend.position = "top"
) +
# flip the chart horizontally
coord_flip()

# create a bar plot to easily compare time
barplotData <- rbind(
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$mean_time_P,
    treatment = "pattern"
  ),
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$mean_time_AP,
    treatment = "antipattern"
  )
) %>% arrange(factor(rule, levels = rev(p))) %>%
  mutate(index = row_number())

# use ggplot to print the grouped bar chart
ggplot(barplotData, aes(x = reorder(rule, index), y = value, fill = treatment)) +
geom_bar(
  stat = "identity",
  width = 0.5,
  position = position_dodge(0.6)
) +
# colors for "rule" and "violation"
scale_fill_manual(values = c( "#dd1100", "#0077dd")) +
# control space for the labels
scale_y_continuous(expand = expansion(mult = c(0, .1))) +
# bar label text and positioning
geom_text(
  aes(label = sprintf("%.1f", round(value, 1))),
  position = position_dodge(0.6),
  fontface = "bold",
  size = 5,
  hjust = -0.05
) +
theme_classic() +
labs(x = "Rule", y = "Mean time to answer in seconds", fill = "") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 16),
  axis.text.x = element_text(size = 14),
  axis.text.y = element_text(size = 14),
  legend.title = element_text(size = 16),
  legend.text = element_text(size = 16),
  legend.position = "top"
) +
# flip the chart horizontally
coord_flip()

# create a bar plot to easily compare TAU
barplotData <- rbind(
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$mean_TAU_P,
    treatment = "Pattern"
  ),
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$mean_TAU_AP,
    treatment = "Antipattern"
  )
) %>% arrange(factor(rule, levels = rev(p))) %>%
  mutate(index = row_number())

# use ggplot to print the grouped bar chart
ggplot(barplotData, aes(x = reorder(rule, index), y = value, fill = treatment)) +
geom_bar(
  stat = "identity",
  width = 0.5,
  position = position_dodge(0.6)
) +
# colors for "rule" and "violation"
scale_fill_manual(values = c("#dd1100", "#0077dd")) +
# control space for the labels
scale_y_continuous(expand = expansion(mult = c(0, .1))) +
# bar label text and positioning
geom_text(
  aes(label = sprintf("%.2f", round(value, 2))),
  position = position_dodge(0.6),
  size = 5,
  fontface = "bold",
  hjust = -0.05
) +
theme_classic() +
labs(x = "Rule", y = "Mean TAU", fill = "") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 16),
  axis.text.x = element_text(size = 14),
  axis.text.y = element_text(size = 14),
  legend.title = element_text(size = 16),
  legend.text = element_text(size = 16),
  legend.position = "top"
) +
# flip the chart horizontally
coord_flip()

# create 2 new data frames for multiple strip plots in one diagram
# each with attributes `TAU`, `version` (1 or 2), and `ruleGroup` (1 to 7)

# "Amorphous", "Contextless", "CRUDy", "Inconsistent", "NonDescriptive", "NonHierarchical", "NonPertinent"
stripPlotData <- rbind(
  data %>% select(TAU_Tidy) %>% filter(!is.na(TAU_Tidy)) %>%
    mutate(version = 1, ruleGroup = 1) %>% rename(TAU = TAU_Tidy),
  data %>% select(TAU_Amorphous) %>% filter(!is.na(TAU_Amorphous)) %>%
    mutate(version = 2, ruleGroup = 1) %>% rename(TAU = TAU_Amorphous),
  data %>% select(TAU_Contextual) %>% filter(!is.na(TAU_Contextual)) %>%
    mutate(version = 1, ruleGroup = 2) %>% rename(TAU = TAU_Contextual),
  data %>% select(TAU_Contextless) %>% filter(!is.na(TAU_Contextless)) %>%
    mutate(version = 2, ruleGroup = 2) %>% rename(TAU = TAU_Contextless),
  data %>% select(TAU_Verbless) %>% filter(!is.na(TAU_Verbless)) %>%
    mutate(version = 1, ruleGroup = 3) %>% rename(TAU = TAU_Verbless),
  data %>% select(TAU_CRUDy) %>% filter(!is.na(TAU_CRUDy)) %>%
    mutate(version = 2, ruleGroup = 3) %>% rename(TAU = TAU_CRUDy),
  data %>% select(TAU_Consistent) %>% filter(!is.na(TAU_Consistent)) %>%
    mutate(version = 1, ruleGroup = 4) %>% rename(TAU = TAU_Consistent),
  data %>% select(TAU_Inconsistent) %>% filter(!is.na(TAU_Inconsistent)) %>%
    mutate(version = 1, ruleGroup = 4) %>% rename(TAU = TAU_Inconsistent),
  data %>% select(TAU_Descriptive) %>% filter(!is.na(TAU_Descriptive)) %>%
    mutate(version = 2, ruleGroup = 5) %>% rename(TAU = TAU_Descriptive),
  data %>% select(TAU_NonDescriptive) %>% filter(!is.na(TAU_NonDescriptive)) %>%
    mutate(version = 2, ruleGroup = 5) %>% rename(TAU = TAU_NonDescriptive),
  data %>% select(TAU_Hierarchical) %>% filter(!is.na(TAU_Hierarchical)) %>%
    mutate(version = 1, ruleGroup = 6) %>% rename(TAU = TAU_Hierarchical),
  data %>% select(TAU_NonHierarchical) %>% filter(!is.na(TAU_NonHierarchical)) %>%
    mutate(version = 1, ruleGroup = 6) %>% rename(TAU = TAU_NonHierarchical),
  data %>% select(TAU_Pertinent) %>% filter(!is.na(TAU_Pertinent)) %>%
    mutate(version = 2, ruleGroup = 7) %>% rename(TAU = TAU_Pertinent),
  data %>% select(TAU_NonPertinent) %>% filter(!is.na(TAU_NonPertinent)) %>%
    mutate(version = 2, ruleGroup = 7) %>% rename(TAU = TAU_NonPertinent)
) %>%
  mutate(version = factor(version, levels = c(1, 2), labels = c("P", "AP"))) %>%
  mutate(ruleGroup = factor(ruleGroup, levels = c(1:7), labels = c("#1: Tidy", "#2: Contextual", "#3: Verbless", "#4: Consistent", "#5: Descriptive", "#6: NonHierarchical", "#7: Pertinent")))

print(stripPlotData)

ggplot(stripPlotData, aes(x = version, y = TAU, fill = ruleGroup)) +
geom_jitter(aes(color = version), width = .25) +
theme_classic() +
# group by rule
facet_grid(. ~ ruleGroup) +
# set color scale for versions
scale_color_manual(values = c("#0077dd", "#dd1100")) +
# set scale for y axis
ylim(0.00, 1.00) +
# add median with special color
stat_summary(fun = "median", geom = "point", shape = 16, size = 7, color = "#ffa600d8") +
labs(x = "Patterns and Antipatterns", y = "TAU") +
theme(
  text = element_text(size = 14, face = "bold", family = "sans"),
  axis.title = element_text(size = 14),
  axis.text.x = element_text(size = 12),
  axis.text.y = element_text(size = 10),
  legend.position = "none"
)

# rules NoTunnel, GETRetrieve, POSTCreate, NoRC200Error, RC401, and RC415
# "NonStandard", "Pluralized", "Unversioned", "Tunneling", "InconArchetype", "Ambiguity", "Flat"
stripPlotData <- rbind(
  data %>% select(TAU_Standard) %>% filter(!is.na(TAU_Standard)) %>%
    mutate(version = 1, ruleGroup = 1) %>% rename(TAU = TAU_Standard),
  data %>% select(TAU_NonStandard) %>% filter(!is.na(TAU_NonStandard)) %>%
    mutate(version = 2, ruleGroup = 1) %>% rename(TAU = TAU_NonStandard),
  data %>% select(TAU_Singularized) %>% filter(!is.na(TAU_Singularized)) %>%
    mutate(version = 1, ruleGroup = 2) %>% rename(TAU = TAU_Singularized),
  data %>% select(TAU_Pluralized) %>% filter(!is.na(TAU_Pluralized)) %>%
    mutate(version = 2, ruleGroup = 2) %>% rename(TAU = TAU_Pluralized),
  data %>% select(TAU_Versioned) %>% filter(!is.na(TAU_Versioned)) %>%
    mutate(version = 1, ruleGroup = 3) %>% rename(TAU = TAU_Versioned),
  data %>% select(TAU_Unversioned) %>% filter(!is.na(TAU_Unversioned)) %>%
    mutate(version = 1, ruleGroup = 3) %>% rename(TAU = TAU_Unversioned),
  data %>% select(TAU_Adherence) %>% filter(!is.na(TAU_Adherence)) %>%
    mutate(version = 2, ruleGroup = 4) %>% rename(TAU = TAU_Adherence),
  data %>% select(TAU_Tunneling) %>% filter(!is.na(TAU_Tunneling)) %>%
    mutate(version = 1, ruleGroup = 4) %>% rename(TAU = TAU_Tunneling),
  data %>% select(TAU_ConArchetype) %>% filter(!is.na(TAU_ConArchetype)) %>%
    mutate(version = 2, ruleGroup = 5) %>% rename(TAU = TAU_ConArchetype),
  data %>% select(TAU_InconArchetype) %>% filter(!is.na(TAU_InconArchetype)) %>%
    mutate(version = 2, ruleGroup = 5) %>% rename(TAU = TAU_InconArchetype),
  data %>% select(TAU_Annotation) %>% filter(!is.na(TAU_Annotation)) %>%
    mutate(version = 1, ruleGroup = 6) %>% rename(TAU = TAU_Annotation),
  data %>% select(TAU_Ambiguity) %>% filter(!is.na(TAU_Ambiguity)) %>%
    mutate(version = 2, ruleGroup = 6) %>% rename(TAU = TAU_Ambiguity),
  data %>% select(TAU_Structured) %>% filter(!is.na(TAU_Structured)) %>%
    mutate(version = 1, ruleGroup = 7) %>% rename(TAU = TAU_Structured),
  data %>% select(TAU_Flat) %>% filter(!is.na(TAU_Flat)) %>%
    mutate(version = 2, ruleGroup = 7) %>% rename(TAU = TAU_Flat)
) %>%
  mutate(version = factor(version, levels = c(1, 2), labels = c("P", "AP"))) %>%
  mutate(ruleGroup = factor(ruleGroup, levels = c(1:7), labels = c("#8: Standard", "#9: Singularized", "#10: Versioned", "#11: Adherence", "#12: ConsistentArchetype", "#13: Annotation", "14: Structured")))

ggplot(stripPlotData, aes(x = version, y = TAU, fill = ruleGroup)) +
geom_jitter(aes(color = version), width = .25) +
theme_classic() +
# group by rule
facet_grid(. ~ ruleGroup) +
# set color scale for versions
scale_color_manual(values = c("#0077dd", "#dd1100")) +
# set scale for y axis
ylim(0.00, 1.00) +
# add median with special color
stat_summary(fun = "median", geom = "point", shape = 16, size = 8, color = "#ffa600d8") +
labs(x = "Patterns and Antipatterns", y = "TAU") +
theme(
  text = element_text(size = 12, face = "bold", family = "sans"),
  axis.title = element_text(size = 14),
  axis.text.x = element_text(size = 12),
  axis.text.y = element_text(size = 10),
  legend.position = "none"
)

# start hypothesis testing
# due to multiple hypotheses, we will use the Holm-Bonferroni correction to adjust the computed p-values; the confidence level is therefore set to 0.05 here
confLevel <- 0.05

# calculate Wilcoxon–Mann–Whitney test
# standard implementation from the `stats` package (asymptotic approximation with ties)

# for individual rules
testResults <- data.frame()
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varTAUP <- paste("TAU", p, sep = "_")
  varTAUAP <- paste("TAU", ap, sep = "_")
  w <- wilcox.test(
    x = data[[varTAUP]],
    y = data[[varTAUAP]],
    alternative = "greater",
    conf.level = confLevel
  )
  # calculate the effect size with Cohens d
  d <- cohens_d(data[[varTAUP]], data[[varTAUAP]])

  # create results data frame
  rule <- c(p)
  U.value <- c(w$statistic)
  p.value <- c(w$p.value)
  cohens.d <- c(d$Cohens_d)
  testResults <- rbind(testResults,
    data.frame(rule, U.value, p.value, cohens.d),
    make.row.names = FALSE
  )
}

print(testResults)


# adjust p-values with Holm-Bonferroni and format them
testResults <- testResults %>%
  mutate(p.value = format.pval(
      p.adjust(p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  )

print(testResults)

# for all rules combined
w <- wilcox.test(
  x = combinedUndDf$Pattern_TAU,
  y = combinedUndDf$Antipattern_TAU,
  alternative = "greater",
  conf.level = confLevel
)
d <- cohens_d(combinedUndDf$Pattern_TAU, combinedDf$Antipattern_TAU)
rule <- c("All rules combined")
U.value <- c(w$statistic)
p.value <- c(format.pval(w$p.value, digits = 4, eps = 0.001))
cohens.d <- c(d$Cohens_d)
testResults <- rbind(testResults,
  data.frame(rule, U.value, p.value, cohens.d),
  make.row.names = FALSE
)

print(testResults)

# visualize d values with bar plot
barplotData <- testResults %>%
  filter(rule != "All rules combined")

# use ggplot to print the bar chart
ggplot(barplotData, aes(x = reorder(rule, cohens.d), y = cohens.d)) +
geom_bar(
  stat = "identity",
  width = 0.8,
  fill = "#0077dd"
) +
# control space for the labels
scale_y_continuous(expand = expansion(mult = c(0, .1))) +
# bar label text and positioning
geom_text(
  aes(label = sprintf("%.2f", round(cohens.d, 2))),
  size = 5.1,
  fontface = "bold",
  hjust = -0.05
) +
theme_classic() +
labs(x = "Rule", y = "Cohen's d") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 16),
  axis.text.x = element_text(size = 14),
  axis.text.y = element_text(size = 14),
  legend.title = element_text(size = 16),
  legend.text = element_text(size = 16)
) +
# flip the chart horizontally
coord_flip()


###################################################################################################################
# Calculations for RQ2 (differences in perceived understandability and correlations with actual understandability)
###################################################################################################################

# calculate descriptive statistics for perceived understandability ratings
descriptiveStats <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varTAUP <- as.name(paste("TAU", p, sep = "_"))
  varTAUAP <- as.name(paste("TAU", ap, sep = "_"))
  varP <- as.name(paste(varP, "", sep = ""))
  varAP <- as.name(paste(varAP, "", sep = ""))
  varP_rating <- as.name(paste(varP, "URating", sep = ""))
  varAP_rating <- as.name(paste(varAP, "URating", sep = ""))
  descriptiveStats <- rbind(
    descriptiveStats,
    data %>% summarise(
      rule = p,
      median_rating_P := median({{ varP_rating }}, na.rm = TRUE),
      median_rating_AP := median({{ varAP_rating }}, na.rm = TRUE),
      mean_rating_P := round(mean({{ varP_rating }}, na.rm = TRUE), 2),
      mean_rating_AP := round(mean({{ varAP_rating }}, na.rm = TRUE), 2),
      mean_TAU_P := mean({{ varTAUP }}, na.rm = TRUE),
      mean_TAU_AP := mean({{ varTAUAP }}, na.rm = TRUE),
      correctPercent_P := scales::percent(sum({{ varP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varP }})) %>% nrow())),
      correctPercent_AP := scales::percent(sum({{ varAP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varAP }})) %>% nrow()))
    )
  )
}

print(descriptiveStats)

# calculate more detailed descriptive stats per individual rule (min, max, var)
descriptiveStatsDetails <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varP_rating <- as.name(paste(p, "URating", sep = ""))
  varAP_rating <- as.name(paste(ap, "URating", sep = ""))

  descriptiveStatsDetails <- rbind(
    descriptiveStatsDetails,
    data %>% summarise(
      rule = p,
      min_rating_P := min({{ varP_rating }}, na.rm = TRUE),
      min_rating_AP := min({{ varAP_rating }}, na.rm = TRUE),
      max_rating_P := max({{ varP_rating }}, na.rm = TRUE),
      max_rating_AP := max({{ varAP_rating }}, na.rm = TRUE),
      var_rating_P := var({{ varP_rating }}, na.rm = TRUE),
      var_rating_AP := var({{ varAP_rating }}, na.rm = TRUE)
    )
  )
}

print(descriptiveStatsDetails)

# create custom likert plots for perceived understandability ratings
ratings <- data.frame()
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- as.name(paste(p, "URating", sep = ""))
  varRatingAP <- as.name(paste(ap, "URating", sep = ""))
  P1 <- data %>% filter({{ varRatingP }} == 1) %>% nrow() * -1
  P2 <- data %>% filter({{ varRatingP }} == 2) %>% nrow() * -1
  AP1 <- data %>% filter({{ varRatingAP }} == 1) %>% nrow()
  AP2 <- data %>% filter({{ varRatingAP }} == 2) %>% nrow()

  ratings <- rbind(ratings,
    data.frame(
      rule = as.character(p),
      countP1 = P1,
      countP2 = P2,
      countAP1 = AP1,
      countAP2 = AP2
    )
  )
}

print(ratings)

# melt the data frame into long format and create factor for ratings
ratings_long <- reshape2::melt(ratings, id.vars = "rule")
ratings_long$variable <- factor(
  ratings_long$variable,
  levels = c("countP1", "countP2", "countAP1", "countAP2"),
  labels = c("Very easy (pattern)", "Easy (pattern)", "Very easy (antipattern)", "Easy (antipattern)")
)

print(ratings_long)

# order according to categories
ratings_long <- ratings_long %>%
  arrange(factor(rule, levels = rev(p))) %>%
  mutate(index = row_number())

print(ratings_long)

# create break values to avoid negative numbers
break_values <- append(pretty(ratings_long$value), c(30, 40, 50))

# create the plot
ggplot(ratings_long, aes(x = reorder(rule, index), y = value, fill = variable)) +
geom_bar(stat = "identity") +
theme_classic() +
# hide y axis
theme(
  axis.line.y = element_blank(),
  axis.ticks.y = element_blank()
) +
labs(x = "Rule", y = "# of ratings per difficulty level", fill = "") +
# set absolute numbers to avoid negatives and stretch axis the same in both directions
scale_y_continuous(
  limits = c(-51, 51),
  breaks = break_values,
  labels = abs(break_values)
) +
# colors for the 4 counts
scale_fill_manual(values = c("#0077dd", "lightblue", "#dd1100", "#ff7e73")) +
# bar label text and positioning
geom_text(
  aes(label = abs(value)),
  position = position_stack(vjust = 0.5),
  fontface = "bold",
  size = 5.5,
  color = "white"
) +
# add vertical line in the middle
geom_hline(yintercept = 0, size = 0.75) +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 18),
  axis.text.x = element_text(size = 16),
  axis.text.y = element_text(size = 16),
  legend.text = element_text(size = 16),
  legend.position = "top"
) +
# flip the chart horizontally
coord_flip()





# start hypothesis testing
# due to multiple hypotheses, we will use the Holm-Bonferroni correction to adjust the computed p-values; the confidence level is therefore set to 0.05 here
confLevel <- 0.05

# calculate Wilcoxon–Mann–Whitney test
# standard implementation from the `stats` package (asymptotic approximation with ties)
testResults <- data.frame()

# for individual rules
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- paste(p, "URating", sep = "")
  varRatingAP <- paste(ap, "URating", sep = "")
  w <- wilcox.test(
    x = data[[varRatingAP]],
    y = data[[varRatingP]],
    alternative = "greater",
    conf.level = confLevel
  )
  
  # calculate the effect size with Cohens d
  d <- cohens_d(data[[varRatingAP]], data[[varRatingP]])
  #print(d)
  

  # create results data frame
  rule <- c(p)
  U.value <- c(w$statistic)
  p.value <- c(w$p.value)
  cohens.d <- c(d$Cohens_d)
  testResults <- rbind(testResults,
    data.frame(rule, U.value, p.value, cohens.d),
    make.row.names = FALSE
  )
}

print(testResults)

# adjust p-values with Holm-Bonferroni and format them
testResults <- testResults %>%
  mutate(p.value = format.pval(
      p.adjust(p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  )



# for all rules combined
w <- wilcox.test(
  x = combinedUndDf$Pattern_rating,
  y = combinedUndDf$Antipattern_rating,
  alternative = "greater",
  conf.level = confLevel
)
d <- cohens_d(combinedUndDf$Pattern_rating, combinedUndDf$Antipattern_rating)
rule <- c("All rules combined")
U.value <- c(w$statistic)
p.value <- c(format.pval(w$p.value, digits = 4, eps = 0.001))
cohens.d <- c(d$Cohens_d)
testResults <- rbind(testResults,
  data.frame(rule, U.value, p.value, cohens.d),
  make.row.names = FALSE
)

print(testResults)

# visualize d values with bar plot
barplotData <- testResults %>%
  filter(rule != "All rules combined")

# use ggplot to print the bar chart
ggplot(barplotData, aes(x = reorder(rule, cohens.d), y = cohens.d)) +
geom_bar(
  stat = "identity",
  width = 0.8,
  fill = "#0077dd"
) +
# control space for the labels
scale_y_continuous(expand = expansion(mult = c(0, .1))) +
# bar label text and positioning
geom_text(
  aes(label = sprintf("%.2f", round(cohens.d, 2))),
  size = 5.1,
  fontface = "bold",
  hjust = -0.05
) +
theme_classic() +
labs(x = "Rule", y = "Cohen's d") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 16),
  axis.text.x = element_text(size = 14),
  axis.text.y = element_text(size = 14),
  legend.title = element_text(size = 16),
  legend.text = element_text(size = 16)
) +
# flip the chart horizontally
coord_flip()

# calculate correlation between perceived understandability and actual understandability (TAU)
correlationUndResults <- data.frame()
corrMthd <- "kendall"

# for each individual rule
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- paste(p, "URating", sep = "")
  varRatingAP <- paste(ap, "URating", sep = "")
  varTAUP <- paste("TAU", p, sep = "_")
  varTAUAP <- paste("TAU", ap, sep = "_")

  corP <- cor.test(
    data[[varRatingP]],
    data[[varTAUP]],
    method = corrMthd,
    alternative = "less",
    conf.level = confLevel
  )
  corAP <- cor.test(
    data[[varRatingAP]],
    data[[varTAUAP]],
    method = corrMthd,
    alternative = "less",
    conf.level = confLevel
  )
  correlationUndResults <- rbind(correlationUndResults,
    data.frame(
      rule = p,
      P_correlation = corP$estimate,
      P_p.value = corP$p.value,
      AP_correlation = corAP$estimate,
      AP_p.value = corAP$p.value
    ),
    make.row.names = FALSE
  )
}

print(correlationUndResults)

# adjust p-values with Holm-Bonferroni and format them
correlationUndResults <- correlationUndResults %>%
  mutate(P_p.value = format.pval(
      p.adjust(P_p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  ) %>%
  mutate(AP_p.value = format.pval(
      p.adjust(AP_p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  )
print(correlationUndResults)

# for all rules combined
corFR <- cor.test(
  combinedUndDf$Pattern_rating,
  combinedUndDf$Pattern_TAU,
  method = corrMthd,
  alternative = "less",
  conf.level = confLevel
)
corIR <- cor.test(
  combinedUndDf$Antipattern_rating,
  combinedUndDf$Antipattern_TAU,
  method = corrMthd,
  alternative = "less",
  conf.level = confLevel
)
correlationUndResults <- rbind(correlationUndResults,
  data.frame(
    rule = "All rules combined",
    P_correlation = corP$estimate,
    P_p.value = format.pval(corP$p.value, digits = 4, eps = 0.001),
    AP_correlation = corAP$estimate,
    AP_p.value = format.pval(corAP$p.value, digits = 4, eps = 0.001)
  ),
  make.row.names = FALSE
)

print(correlationUndResults)

# regression results for each individual rule
df <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- paste(p, "URating", sep = "")
  varRatingAP <- paste(ap, "URating", sep = "")
  varTAUP <- paste("TAU", p, sep = "_")
  varTAUAP <- paste("TAU", ap, sep = "_")

  resP <- lm(
    as.formula(paste(varTAUP, "~", varRatingP)),
    data = data
  )
  resAP <- lm(
    as.formula(paste(varTAUAP, "~", varRatingAP)),
    data = data
  )
  df <- rbind(df,
    data.frame(
      rule = ap,
      P_adjustedR2 = summary(resP)$adj.r.squared,
      P_p.value = format.pval(summary(resP)$coefficients[8], digits = 4, eps = 0.001),
      AP_adjustedR2 = summary(resAP)$adj.r.squared,
      AP_p.value = format.pval(summary(resAP)$coefficients[8], digits = 4, eps = 0.001)
    ),
    make.row.names = FALSE
  )
}
print(df)

df %>% arrange(AP_adjustedR2) %>%
  print

# visualize adjusted R-squared values for violation
barplotData <- df %>%
  select(rule, AP_adjustedR2)

# use ggplot to print the bar chart
ggplot(barplotData, aes(x = reorder(rule, AP_adjustedR2), y = AP_adjustedR2)) +
geom_bar(
  stat = "identity",
  width = 0.8,
  fill = "#dd1100"
) +
# control space for the labels
scale_y_continuous(expand = expansion(mult = c(0.01, 0.12))) +
# bar label text and positioning
geom_text(
  aes(
    label = sprintf("%.2f", round(AP_adjustedR2, 2)),
    # fix label placement for negative numbers
    y = ifelse(AP_adjustedR2 > 0, AP_adjustedR2 + 0.001, AP_adjustedR2 - 0.025)
  ),
  size = 5,
  fontface = "bold",
  hjust = -0.05
) +
theme_classic() +
labs(x = "Rule", y = "Adjusted R-squared") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 16),
  axis.text.x = element_text(size = 14),
  axis.text.y = element_text(size = 14),
  legend.title = element_text(size = 16),
  legend.text = element_text(size = 16)
) +
# flip the chart horizontally
coord_flip()


###################################################################################################################
# Calculations for RQ3 (differences in perceived readability and correlations with actual understandability)
###################################################################################################################

# calculate descriptive statistics for perceived readability ratings

descriptiveStats <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varTAUP <- as.name(paste("TAU", p, sep = "_"))
  varTAUAP <- as.name(paste("TAU", ap, sep = "_"))
  varP <- as.name(paste(varP, "", sep = ""))
  varAP <- as.name(paste(varAP, "", sep = ""))
  varP_rating <- as.name(paste(varP, "RRating", sep = ""))
  varAP_rating <- as.name(paste(varAP, "RRating", sep = ""))
  descriptiveStats <- rbind(
    descriptiveStats,
    data %>% summarise(
      rule = p,
      median_rating_P := median({{ varP_rating }}, na.rm = TRUE),
      median_rating_AP := median({{ varAP_rating }}, na.rm = TRUE),
      mean_rating_P := round(mean({{ varP_rating }}, na.rm = TRUE), 2),
      mean_rating_AP := round(mean({{ varAP_rating }}, na.rm = TRUE), 2),
      mean_TAU_P := mean({{ varTAUP }}, na.rm = TRUE),
      mean_TAU_AP := mean({{ varTAUAP }}, na.rm = TRUE),
      correctPercent_P := scales::percent(sum({{ varP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varP }})) %>% nrow())),
      correctPercent_AP := scales::percent(sum({{ varAP }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varAP }})) %>% nrow()))
    )
  )
}

print(descriptiveStats)

# calculate more detailed descriptive stats per individual rule (min, max, var)
descriptiveStatsDetails <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varP_rating <- as.name(paste(p, "RRating", sep = ""))
  varAP_rating <- as.name(paste(ap, "RRating", sep = ""))
  
  descriptiveStatsDetails <- rbind(
    descriptiveStatsDetails,
    data %>% summarise(
      rule = p,
      min_rating_P := min({{ varP_rating }}, na.rm = TRUE),
      min_rating_AP := min({{ varAP_rating }}, na.rm = TRUE),
      max_rating_P := max({{ varP_rating }}, na.rm = TRUE),
      max_rating_AP := max({{ varAP_rating }}, na.rm = TRUE),
      var_rating_P := var({{ varP_rating }}, na.rm = TRUE),
      var_rating_AP := var({{ varAP_rating }}, na.rm = TRUE)
    )
  )
}

print(descriptiveStatsDetails)

# create custom likert plots for perceived readability ratings
ratings <- data.frame()
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- as.name(paste(p, "RRating", sep = ""))
  varRatingAP <- as.name(paste(ap, "RRating", sep = ""))
  P1 <- data %>% filter({{ varRatingP }} == 1) %>% nrow() * -1
  P2 <- data %>% filter({{ varRatingP }} == 2) %>% nrow() * -1
  AP1 <- data %>% filter({{ varRatingAP }} == 1) %>% nrow()
  AP2 <- data %>% filter({{ varRatingAP }} == 2) %>% nrow()
  
  ratings <- rbind(ratings,
                   data.frame(
                     rule = as.character(p),
                     countP1 = P1,
                     countP2 = P2,
                     countAP1 = AP1,
                     countAP2 = AP2
                   )
  )
}

print(ratings)

# melt the data frame into long format and create factor for ratings
ratings_long <- reshape2::melt(ratings, id.vars = "rule")
ratings_long$variable <- factor(
  ratings_long$variable,
  levels = c("countP1", "countP2", "countAP1", "countAP2"),
  labels = c("Very easy (pattern)", "Easy (pattern)", "Very easy (antipattern)", "Easy (antipattern)")
)

print(ratings_long)

# order according to categories
ratings_long <- ratings_long %>%
  arrange(factor(rule, levels = rev(p))) %>%
  mutate(index = row_number())

print(ratings_long)

# create break values to avoid negative numbers
break_values <- append(pretty(ratings_long$value), c(30, 40, 50))

# create the plot
ggplot(ratings_long, aes(x = reorder(rule, index), y = value, fill = variable)) +
  geom_bar(stat = "identity") +
  theme_classic() +
  # hide y axis
  theme(
    axis.line.y = element_blank(),
    axis.ticks.y = element_blank()
  ) +
  labs(x = "Rule", y = "# of ratings per readability level", fill = "") +
  # set absolute numbers to avoid negatives and stretch axis the same in both directions
  scale_y_continuous(
    limits = c(-51, 51),
    breaks = break_values,
    labels = abs(break_values)
  ) +
  # colors for the 4 counts
  scale_fill_manual(values = c("#0077dd", "lightblue", "#dd1100", "#ff7e73")) +
  # bar label text and positioning
  geom_text(
    aes(label = abs(value)),
    position = position_stack(vjust = 0.5),
    fontface = "bold",
    size = 5.5,
    color = "white"
  ) +
  # add vertical line in the middle
  geom_hline(yintercept = 0, size = 0.75) +
  theme(
    text = element_text(size = 16, face = "bold", family = "sans"),
    axis.title = element_text(size = 18),
    axis.text.x = element_text(size = 16),
    axis.text.y = element_text(size = 16),
    legend.text = element_text(size = 16),
    legend.position = "top"
  ) +
  # flip the chart horizontally
  coord_flip()

# start hypothesis testing
# due to multiple hypotheses, we will use the Holm-Bonferroni correction to adjust the computed p-values; the confidence level is therefore set to 0.05 here
confLevel <- 0.05

# calculate Wilcoxon–Mann–Whitney test
# standard implementation from the `stats` package (asymptotic approximation with ties)
testResults <- data.frame()

# for individual rules
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- paste(p, "RRating", sep = "")
  varRatingAP <- paste(ap, "RRating", sep = "")
  w <- wilcox.test(
    x = data[[varRatingAP]],
    y = data[[varRatingP]],
    alternative = "greater",
    conf.level = confLevel
  )
  
  # calculate the effect size with Cohens d
  d <- cohens_d(data[[varRatingAP]], data[[varRatingP]])
  #print(d)
  
  
  # create results data frame
  rule <- c(p)
  U.value <- c(w$statistic)
  p.value <- c(w$p.value)
  cohens.d <- c(d$Cohens_d)
  testResults <- rbind(testResults,
                       data.frame(rule, U.value, p.value, cohens.d),
                       make.row.names = FALSE
  )
}

print(testResults)

# adjust p-values with Holm-Bonferroni and format them
testResults <- testResults %>%
  mutate(p.value = format.pval(
    p.adjust(p.value, method = "holm"),
    digits = 4, eps = 0.001
  )
  )



# for all rules combined
w <- wilcox.test(
  x = combinedReadDf$Pattern_rating,
  y = combinedReadDf$Antipattern_rating,
  alternative = "greater",
  conf.level = confLevel
)
d <- cohens_d(combinedReadDf$Pattern_rating, combinedReadDf$Antipattern_rating)
rule <- c("All rules combined")
U.value <- c(w$statistic)
p.value <- c(format.pval(w$p.value, digits = 4, eps = 0.001))
cohens.d <- c(d$Cohens_d)
testResults <- rbind(testResults,
                     data.frame(rule, U.value, p.value, cohens.d),
                     make.row.names = FALSE
)

print(testResults)

# visualize d values with bar plot
barplotData <- testResults %>%
  filter(rule != "All rules combined")

# use ggplot to print the bar chart
ggplot(barplotData, aes(x = reorder(rule, cohens.d), y = cohens.d)) +
  geom_bar(
    stat = "identity",
    width = 0.8,
    fill = "#0077dd"
  ) +
  # control space for the labels
  scale_y_continuous(expand = expansion(mult = c(0, .1))) +
  # bar label text and positioning
  geom_text(
    aes(label = sprintf("%.2f", round(cohens.d, 2))),
    size = 5.1,
    fontface = "bold",
    hjust = -0.05
  ) +
  theme_classic() +
  labs(x = "Rule", y = "Cohen's d") +
  theme(
    text = element_text(size = 16, face = "bold", family = "sans"),
    axis.title = element_text(size = 16),
    axis.text.x = element_text(size = 14),
    axis.text.y = element_text(size = 14),
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 16)
  ) +
  # flip the chart horizontally
  coord_flip()

# calculate correlation between perceived readability and actual understandability (TAU)
correlationReadResults <- data.frame()
corrMthd <- "kendall"

# for each individual rule
for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- paste(p, "RRating", sep = "")
  varRatingAP <- paste(ap, "RRating", sep = "")
  varTAUP <- paste("TAU", p, sep = "_")
  varTAUAP <- paste("TAU", ap, sep = "_")
  
  corP <- cor.test(
    data[[varRatingP]],
    data[[varTAUP]],
    method = corrMthd,
    alternative = "less",
    conf.level = confLevel
  )
  corAP <- cor.test(
    data[[varRatingAP]],
    data[[varTAUAP]],
    method = corrMthd,
    alternative = "less",
    conf.level = confLevel
  )
  correlationReadResults <- rbind(correlationReadResults,
                              data.frame(
                                rule = p,
                                P_correlation = corP$estimate,
                                P_p.value = corP$p.value,
                                AP_correlation = corAP$estimate,
                                AP_p.value = corAP$p.value
                              ),
                              make.row.names = FALSE
  )
}

print(correlationReadResults)

# adjust p-values with Holm-Bonferroni and format them
correlationReadResults <- correlationReadResults %>%
  mutate(P_p.value = format.pval(
    p.adjust(P_p.value, method = "holm"),
    digits = 4, eps = 0.001
  )
  ) %>%
  mutate(AP_p.value = format.pval(
    p.adjust(AP_p.value, method = "holm"),
    digits = 4, eps = 0.001
  )
  )
print(correlationReadResults)

# for all rules combined
corFR <- cor.test(
  combinedReadDf$Pattern_rating,
  combinedReadDf$Pattern_TAU,
  method = corrMthd,
  alternative = "less",
  conf.level = confLevel
)
corIR <- cor.test(
  combinedReadDf$Antipattern_rating,
  combinedReadDf$Antipattern_TAU,
  method = corrMthd,
  alternative = "less",
  conf.level = confLevel
)
correlationReadResults <- rbind(correlationReadResults,
                            data.frame(
                              rule = "All rules combined",
                              P_correlation = corP$estimate,
                              P_p.value = format.pval(corP$p.value, digits = 4, eps = 0.001),
                              AP_correlation = corAP$estimate,
                              AP_p.value = format.pval(corAP$p.value, digits = 4, eps = 0.001)
                            ),
                            make.row.names = FALSE
)

print(correlationReadResults)

# regression results for each individual rule
df <- data.frame()

for (i in seq_along(patterns)) {
  p <- patterns[i]
  ap <- antipatterns[i]
  varRatingP <- paste(p, "RRating", sep = "")
  varRatingAP <- paste(ap, "RRating", sep = "")
  varTAUP <- paste("TAU", p, sep = "_")
  varTAUAP <- paste("TAU", ap, sep = "_")
  
  resP <- lm(
    as.formula(paste(varTAUP, "~", varRatingP)),
    data = data
  )
  resAP <- lm(
    as.formula(paste(varTAUAP, "~", varRatingAP)),
    data = data
  )
  df <- rbind(df,
              data.frame(
                rule = ap,
                P_adjustedR2 = summary(resP)$adj.r.squared,
                P_p.value = format.pval(summary(resP)$coefficients[8], digits = 4, eps = 0.001),
                AP_adjustedR2 = summary(resAP)$adj.r.squared,
                AP_p.value = format.pval(summary(resAP)$coefficients[8], digits = 4, eps = 0.001)
              ),
              make.row.names = FALSE
  )
}
print(df)

df %>% arrange(AP_adjustedR2) %>%
  print

# visualize adjusted R-squared values for violation
barplotData <- df %>%
  select(rule, AP_adjustedR2)

# use ggplot to print the bar chart
ggplot(barplotData, aes(x = reorder(rule, AP_adjustedR2), y = AP_adjustedR2)) +
  geom_bar(
    stat = "identity",
    width = 0.8,
    fill = "#dd1100"
  ) +
  # control space for the labels
  scale_y_continuous(expand = expansion(mult = c(0.01, 0.12))) +
  # bar label text and positioning
  geom_text(
    aes(
      label = sprintf("%.2f", round(AP_adjustedR2, 2)),
      # fix label placement for negative numbers
      y = ifelse(AP_adjustedR2 > 0, AP_adjustedR2 + 0.001, AP_adjustedR2 - 0.025)
    ),
    size = 5,
    fontface = "bold",
    hjust = -0.05
  ) +
  theme_classic() +
  labs(x = "Rule", y = "Adjusted R-squared") +
  theme(
    text = element_text(size = 16, face = "bold", family = "sans"),
    axis.title = element_text(size = 16),
    axis.text.x = element_text(size = 14),
    axis.text.y = element_text(size = 14),
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 16)
  ) +
  # flip the chart horizontally
  coord_flip()

#########################################################################################################
# Calculations for RQ4 (How does REST related experience influence the results of RQ1, RQ2, and RQ3)
#########################################################################################################
# variable names for the antipatterns


# aggregate mean values for TAU, perceived understandability, correctness, and time (needed for RQ4)
correlationUndData <- data %>%
  rowwise() %>%
  mutate(
    mean_TAU_P = ifelse(
      mean(c(TAU_Tidy, TAU_Contextual, TAU_Verbless, TAU_Consistent, TAU_Descriptive, TAU_Hierarchical, TAU_Pertinent), na.rm = TRUE),
      mean(c(TAU_Standard, TAU_Singularized, TAU_Versioned, TAU_Adherence, TAU_ConArchetype, TAU_Annotation, TAU_Structured), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_TAU_AP = 
      mean(c(TAU_Amorphous, TAU_Contextless, TAU_CRUDy, TAU_Inconsistent, TAU_NonDescriptive, TAU_NonHierarchical, TAU_NonPertinent), na.rm = TRUE),
      mean(c(TAU_NonStandard, TAU_Pluralized, TAU_Unversioned, TAU_Tunneling, TAU_InconArchetype, TAU_Ambiguity, TAU_Flat), na.rm = TRUE)
  ) %>%
  mutate(
    mean_perceivedDifficulty_P = ifelse(
      mean(c(TidyURating, ContextualURating, VerblessURating, ConsistentURating, DescriptiveURating, HierarchicalURating, PertinentURating), na.rm = TRUE),
      mean(c(StandardURating, SingularizedURating, VersionedURating, AdherenceURating, ConArchetypeURating, AnnotationURating, StructuredURating), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_perceivedDifficulty_AP = ifelse(
      mean(c(AmorphousURating, ContextlessURating, CRUDyURating, InconsistentURating, NonDescriptiveURating, NonHierarchicalURating, NonPertinentURating), na.rm = TRUE),
      mean(c(NonStandardURating, PluralizedURating, UnversionedURating, TunnelingURating, InconArchetypeURating, AmbiguityURating, FlatURating), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Time_P = ifelse(
      mean(c(TidyTime, ContextualURating, VerblessTime, ConsistentTime, DescriptiveTime, HierarchicalTime, PertinentTime), na.rm = TRUE),
      mean(c(StandardTime, SingularizedTime, VersionedTime, AdherenceTime, ConArchetypeTime, AnnotationTime, StructuredTime), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Time_AP = 
      mean(c(AmorphousTime, ContextlessTime, CRUDyTime, InconsistentTime, NonDescriptiveTime, NonHierarchicalTime, NonPertinentTime), na.rm = TRUE),
      mean(c(NonStandardTime, PluralizedTime, VersionedTime, TunnelingTime, InconArchetypeTime, AmbiguityTime, FlatTime), na.rm = TRUE)
    
  ) %>%
  mutate(
    mean_Corr_P = ifelse(
      mean(c(Tidy, Contextual, Verbless, Consistent, Descriptive, Hierarchical, Pertinent), na.rm = TRUE),
      mean(c(Standard, Singularized, Versioned, Adherence, ConArchetype, Annotation, Structured), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Corr_AP = 
      mean(c(Amorphous, Contextless, CRUDy, Inconsistent, NonDescriptive, NonHierarchical, NonPertinent), na.rm = TRUE),
      mean(c(NonStandard, Pluralized, Unversioned, Tunneling, InconArchetype, Ambiguity, Flat), na.rm = TRUE)
    
  )
print(correlationUndData)
# Correlation matrix for exploration
# rcorr does not support kendalls TAU
# "pearson" for linear correlation of continuous variables
# "spearman" for rank-based monotonic correlation (with ordinal variables)
corrMthd <- "spearman"
corrMatrix <-
  correlationUndData %>%
  select(
    starts_with("mean_"),
    starts_with("is_"),
    YearsOfExperience,
    RichardsonMaturity,
    MaturityLevel
  ) %>%
  as.matrix() %>%
  rcorr(type = corrMthd)

print(corrMatrix)
print(dim(corrMatrix$r))  # Dimensions of the correlation matrix
print(dim(corrMatrix$P))  # Dimensions of the p-value matrix

# plot a correlation matrix
corrplot(corrMatrix$r, p.mat = corrMatrix$P, method = "circle", type = "lower")

print(correlationUndData)
# caculate separate correlations
corrMthd <- "kendall"
df <- data.frame()
# change to "mean_TAU_P", "mean_TAU_AP", "mean_perceivedDifficulty_P", or "mean_perceivedDifficulty_AP"
dependent <- "mean_TAU_P"
demographics <- c("is_Student", "is_Academia", "is_Canada", "YearsOfExperience", "RichardsonMaturity", "MaturityLevel")

for (d in demographics) {
  res <- cor.test(
      correlationUndData[[dependent]],
      correlationUndData[[d]],
      method = corrMthd,
      exact = FALSE
  )
  df <- rbind(df, data.frame(
      dependent = dependent,
      demographic = d,
      estimate = res$estimate,
      p.value = res$p.value
    ),
    make.row.names = FALSE
  )
}

# adjust p-values with Holm-Bonferroni and format them
df %>%
  mutate(p.value = format.pval(
      p.adjust(p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  ) %>%
  arrange(p.value) %>%
  print

# create 2 linear regression models for predicting TAU (one for following patterns and one for followng antipatterns)
# LM for rule:
lrP <- lm(
  mean_TAU_P ~
    is_Student
    + is_Academia
    + is_Canada
    + YearsOfExperience
    + MaturityLevel,
  data = correlationUndData
)
summary(lrP)

# LM for violation:
lrAP <- lm(
  mean_TAU_AP ~
    is_Student
    + is_Academia
    + is_Canada
    + YearsOfExperience
    + MaturityLevel,
  data = correlationUndData
)
summary(lrAP)


# aggregate mean values for TAU, perceived readability, correctness, and time (needed for RQ3)
correlationReadData <- data %>%
  rowwise() %>%
  mutate(
    mean_TAU_P = ifelse(
      mean(c(TAU_Tidy, TAU_Contextual, TAU_Verbless, TAU_Consistent, TAU_Descriptive, TAU_Hierarchical, TAU_Pertinent), na.rm = TRUE),
      mean(c(TAU_Standard, TAU_Singularized, TAU_Versioned, TAU_Adherence, TAU_ConArchetype, TAU_Annotation, TAU_Structured), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_TAU_AP = 
      mean(c(TAU_Amorphous, TAU_Contextless, TAU_CRUDy, TAU_Inconsistent, TAU_NonDescriptive, TAU_NonHierarchical, TAU_NonPertinent), na.rm = TRUE),
    mean(c(TAU_NonStandard, TAU_Pluralized, TAU_Unversioned, TAU_Tunneling, TAU_InconArchetype, TAU_Ambiguity, TAU_Flat), na.rm = TRUE)
  ) %>%
  mutate(
    mean_perceivedReadability_P = ifelse(
      mean(c(TidyRRating, ContextualRRating, VerblessRRating, ConsistentRRating, DescriptiveRRating, HierarchicalRRating, PertinentRRating), na.rm = TRUE),
      mean(c(StandardRRating, SingularizedRRating, VersionedRRating, AdherenceRRating, ConArchetypeRRating, AnnotationRRating, StructuredRRating), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_perceivedReadability_AP = ifelse(
      mean(c(AmorphousRRating, ContextlessRRating, CRUDyRRating, InconsistentRRating, NonDescriptiveRRating, NonHierarchicalRRating, NonPertinentRRating), na.rm = TRUE),
      mean(c(NonStandardRRating, PluralizedRRating, UnversionedRRating, TunnelingRRating, InconArchetypeRRating, AmbiguityRRating, FlatRRating), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Time_P = ifelse(
      mean(c(TidyTime, ContextualURating, VerblessTime, ConsistentTime, DescriptiveTime, HierarchicalTime, PertinentTime), na.rm = TRUE),
      mean(c(StandardTime, SingularizedTime, VersionedTime, AdherenceTime, ConArchetypeTime, AnnotationTime, StructuredTime), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Time_AP = 
      mean(c(AmorphousTime, ContextlessTime, CRUDyTime, InconsistentTime, NonDescriptiveTime, NonHierarchicalTime, NonPertinentTime), na.rm = TRUE),
    mean(c(NonStandardTime, PluralizedTime, VersionedTime, TunnelingTime, InconArchetypeTime, AmbiguityTime, FlatTime), na.rm = TRUE)
    
  ) %>%
  mutate(
    mean_Corr_P = ifelse(
      mean(c(Tidy, Contextual, Verbless, Consistent, Descriptive, Hierarchical, Pertinent), na.rm = TRUE),
      mean(c(Standard, Singularized, Versioned, Adherence, ConArchetype, Annotation, Structured), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Corr_AP = 
      mean(c(Amorphous, Contextless, CRUDy, Inconsistent, NonDescriptive, NonHierarchical, NonPertinent), na.rm = TRUE),
    mean(c(NonStandard, Pluralized, Unversioned, Tunneling, InconArchetype, Ambiguity, Flat), na.rm = TRUE)
    
  )
print(correlationReadData)

# Correlation matrix for exploration
# rcorr does not support kendalls TAU
# "pearson" for linear correlation of continuous variables
# "spearman" for rank-based monotonic correlation (with ordinal variables)
corrMthd <- "spearman"
corrMatrix <-
  correlationReadData %>%
  select(
    starts_with("mean_"),
    starts_with("is_"),
    YearsOfExperience,
    RichardsonMaturity,
    MaturityLevel
  ) %>%
  as.matrix() %>%
  rcorr(type = corrMthd)

print(corrMatrix)
# plot a correlation matrix
corrplot(corrMatrix$r, p.mat = corrMatrix$P, method = "circle", type = "lower")

print(correlationReadData)
# caculate separate correlations
corrMthd <- "kendall"
df <- data.frame()
# change to "mean_TAU_P", "mean_TAU_AP", "mean_perceivedDifficulty_P", or "mean_perceivedDifficulty_AP"
dependent <- "mean_TAU_P"
demographics <- c("is_Student", "is_Academia", "is_Canada", "YearsOfExperience", "RichardsonMaturity", "MaturityLevel")

for (d in demographics) {
  res <- cor.test(
    correlationReadData[[dependent]],
    correlationReadData[[d]],
    method = corrMthd,
    exact = FALSE
  )
  df <- rbind(df, data.frame(
    dependent = dependent,
    demographic = d,
    estimate = res$estimate,
    p.value = res$p.value
  ),
  make.row.names = FALSE
  )
}

# adjust p-values with Holm-Bonferroni and format them
df %>%
  mutate(p.value = format.pval(
    p.adjust(p.value, method = "holm"),
    digits = 4, eps = 0.001
  )
  ) %>%
  arrange(p.value) %>%
  print

# create 2 linear regression models for predicting TAU (one for following patterns and one for followng antipatterns)
# LM for rule:
lrP <- lm(
  mean_TAU_P ~
    is_Student
  + is_Academia
  + is_Canada
  + YearsOfExperience
  + MaturityLevel,
  data = correlationReadData
)
summary(lrP)

# LM for violation:
lrAP <- lm(
  mean_TAU_AP ~
    is_Student
  + is_Academia
  + is_Canada
  + YearsOfExperience
  + MaturityLevel,
  data = correlationReadData
)
summary(lrAP)

