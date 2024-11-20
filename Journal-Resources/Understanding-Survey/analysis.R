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

# info: the abbreviation `FR` stands for "Following Rule", so everything annotated with FR addresses the version that
# adheres to the rules. `IR` stands for "Ignoring Rule", i.e., this addresses the version that violates the rules.

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
data <- read.csv("results.csv", na.strings = c("", "NA"), fileEncoding = "UTF-8-BOM")

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
data %>%
  select(group_id) %>%
  table()

# median participant stats by task order group
data %>%
  group_by(group_id) %>%
  summarise(
    numParticipants = n(),
    medianYearsOfExperience = median(YearsOfExperience, na.rm = TRUE),
    numKnowledgeOfRichardsonMaturityModel = sum(RichardsonMaturity, na.rm = TRUE),
    medianRichardsonMaturityRating = median(MaturityLevel, na.rm = TRUE),
    numStudents = sum(is_Student),
    numAcademia = sum(is_Academia),
    numIndustry = n() - numStudents - numAcademia,
    numGermany = sum(is_Germany)
  )

# variable names for the rules
ruleNames <- c(
  "PluralNoun", "VerbController", "CRUDNames",
  "PathHierarchy1", "PathHierarchy2", "PathHierarchy3",
  "NoTunnel", "GETRetrieve", "POSTCreate",
  "NoRC200Error", "RC401", "RC415"
)

# calculate TAU for every question and both groups
for (var in ruleNames) {
  var <- as.name(var)
  varFR <- as.name(paste(var, "FR", sep = ""))
  varFRTime <- as.name(paste(var, "FRTime", sep = ""))
  varIR <- as.name(paste(var, "IR", sep = ""))
  varIRTime <- as.name(paste(var, "IRTime", sep = ""))
  data <- data %>%
    mutate("TAUFR_{{var}}" := calculateTAU({{ varFR }}, {{ varFRTime }}, max({{ varFRTime }}, {{ varIRTime }}, na.rm = TRUE))) %>%
    mutate("TAUIR_{{var}}" := calculateTAU({{ varIR }}, {{ varIRTime }}, max({{ varFRTime }}, {{ varIRTime }}, na.rm = TRUE)))
}

print(data)
# --> data now has attributes TAUFR_<RuleIdentifier> and TAUIR_<RuleIdentifier>

# create custom data frame with ratings and TAU for all rules combined
combinedDf <- data.frame(matrix(ncol = 4, nrow = 0))
colnames(combinedDf) <- c("FR_rating", "FR_TAU", "IR_rating", "IR_TAU")
for (var in ruleNames) {
  varRatingFR <- paste(var, "FR_rating", sep = "")
  varRatingIR <- paste(var, "IR_rating", sep = "")
  varTAUFR <- paste("TAUFR", var, sep = "_")
  varTAUIR <- paste("TAUIR", var, sep = "_")

  # merge data frames
  combinedDf <- rbind(combinedDf, data.frame(
    FR_rating = data[[varRatingFR]],
    FR_TAU = data[[varTAUFR]],
    IR_rating = data[[varRatingIR]],
    IR_TAU = data[[varTAUIR]]
  ))
}
print(combinedDf)

# Shapiro-Wilk test for non-normal distribution (replace value with the different rule identifiers, i.e., 1 to 12)
var <- ruleNames[1]
varFR <- as.name(paste("TAUFR", var, sep = "_"))
varIR <- as.name(paste("TAUIR", var, sep = "_"))
checkDataDistribution(data[[varFR]], varFR)
checkDataDistribution(data[[varIR]], varIR)

# results: every dataset is not normally distributed --> non-parametric test needed


####################################################################################################
# Calculations for RQ1 (Which design rules have an impact on the understandability of RESTful APIs?)
####################################################################################################

# descriptive statistics

# calculate summary stats for all important performance metrics per individual rule
descriptiveStats <- data.frame()

for (var in ruleNames) {
  varTAUFR <- as.name(paste("TAUFR", var, sep = "_"))
  varTAUIR <- as.name(paste("TAUIR", var, sep = "_"))
  varFR <- as.name(paste(var, "FR", sep = ""))
  varFRTime <- as.name(paste(var, "FRTime", sep = ""))
  varIR <- as.name(paste(var, "IR", sep = ""))
  varIRTime <- as.name(paste(var, "IRTime", sep = ""))
  

  descriptiveStats <- rbind(
    descriptiveStats,
    data %>% summarise(
      rule = var,
      mean_TAU_FR := mean({{ varTAUFR }}, na.rm = TRUE),
      mean_TAU_IR := mean({{ varTAUIR }}, na.rm = TRUE),
      mean_time_FR := mean({{ varFRTime }}, na.rm = TRUE),
      mean_time_IR := mean({{ varIRTime }}, na.rm = TRUE),
      correctAnswers_FR := sum({{ varFR }}, na.rm = TRUE),
      correctAnswers_IR := sum({{ varIR }}, na.rm = TRUE),
      answers_FR := data %>% filter(!is.na({{ varFR }})) %>% nrow(),
      answers_IR := data %>% filter(!is.na({{ varIR }})) %>% nrow(),
      correctPercent_FR := scales::percent(sum({{ varFR }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varFR }})) %>% nrow())),
      correctPercent_IR := scales::percent(sum({{ varIR }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varIR }})) %>% nrow())),
      correctness_FR := sum({{ varFR }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varFR }})) %>% nrow()),
      correctness_IR := sum({{ varIR }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varIR }})) %>% nrow())
    )
  )
}

print(descriptiveStats)

# calculate more detailed descriptive stats per individual rule (min, max, var)
descriptiveStatsDetails <- data.frame()

for (var in ruleNames) {
  varTAUFR <- as.name(paste("TAUFR", var, sep = "_"))
  varTAUIR <- as.name(paste("TAUIR", var, sep = "_"))
  varFR <- as.name(paste(var, "FR", sep = ""))
  varFRTime <- as.name(paste(var, "FRTime", sep = ""))
  varIR <- as.name(paste(var, "IR", sep = ""))
  varIRTime <- as.name(paste(var, "IRTime", sep = ""))

  descriptiveStatsDetails <- rbind(
    descriptiveStatsDetails,
    data %>% summarise(
      rule = var,
      min_TAU_FR := min({{ varTAUFR }}, na.rm = TRUE),
      min_TAU_IR := min({{ varTAUIR }}, na.rm = TRUE),
      max_TAU_FR := max({{ varTAUFR }}, na.rm = TRUE),
      max_TAU_IR := max({{ varTAUIR }}, na.rm = TRUE),
      var_TAU_FR := var({{ varTAUFR }}, na.rm = TRUE),
      var_TAU_IR := var({{ varTAUIR }}, na.rm = TRUE),
      min_time_FR := min({{ varFRTime }}, na.rm = TRUE),
      min_time_IR := min({{ varIRTime }}, na.rm = TRUE),
      max_time_FR := max({{ varFRTime }}, na.rm = TRUE),
      max_time_IR := max({{ varIRTime }}, na.rm = TRUE),
      var_time_FR := var({{ varFRTime }}, na.rm = TRUE),
      var_time_IR := var({{ varIRTime }}, na.rm = TRUE)
    )
  )
}

print(descriptiveStatsDetails)

# create a bar plot to easily compare correctPercent
barplotData <- rbind(
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$correctness_FR,
    treatment = "rule"
  ),
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$correctness_IR,
    treatment = "violation"
  )
) %>% arrange(factor(rule, levels = rev(ruleNames))) %>%
  mutate(index = row_number())

# use ggplot to print the grouped bar chart
ggplot(barplotData, aes(x = reorder(rule, index), y = value, fill = treatment)) +
geom_bar(
  stat = "identity",
  width = 0.5,
  position = position_dodge(0.6)
) +
# colors for "rule" and "violation"
scale_fill_manual(values = c("#0077dd", "#dd1100")) +
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
    value = descriptiveStats$mean_time_FR,
    treatment = "rule"
  ),
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$mean_time_IR,
    treatment = "violation"
  )
) %>% arrange(factor(rule, levels = rev(ruleNames))) %>%
  mutate(index = row_number())

# use ggplot to print the grouped bar chart
ggplot(barplotData, aes(x = reorder(rule, index), y = value, fill = treatment)) +
geom_bar(
  stat = "identity",
  width = 0.5,
  position = position_dodge(0.6)
) +
# colors for "rule" and "violation"
scale_fill_manual(values = c("#0077dd", "#dd1100")) +
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
    value = descriptiveStats$mean_TAU_FR,
    treatment = "rule"
  ),
  data.frame(
    rule = descriptiveStats$rule,
    value = descriptiveStats$mean_TAU_IR,
    treatment = "violation"
  )
) %>% arrange(factor(rule, levels = rev(ruleNames))) %>%
  mutate(index = row_number())

# use ggplot to print the grouped bar chart
ggplot(barplotData, aes(x = reorder(rule, index), y = value, fill = treatment)) +
geom_bar(
  stat = "identity",
  width = 0.5,
  position = position_dodge(0.6)
) +
# colors for "rule" and "violation"
scale_fill_manual(values = c("#0077dd", "#dd1100")) +
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
# each with attributes `TAU`, `version` (1 or 2), and `ruleGroup` (1 to 6)

# rules PluralNoun, VerbController, CRUDNames, PathHierarchy1, PathHierarchy2, and PathHierarchy3
stripPlotData <- rbind(
  data %>% select(TAUFR_PluralNoun) %>% filter(!is.na(TAUFR_PluralNoun)) %>%
    mutate(version = 1, ruleGroup = 1) %>% rename(TAU = TAUFR_PluralNoun),
  data %>% select(TAUIR_PluralNoun) %>% filter(!is.na(TAUIR_PluralNoun)) %>%
    mutate(version = 2, ruleGroup = 1) %>% rename(TAU = TAUIR_PluralNoun),
  data %>% select(TAUFR_VerbController) %>% filter(!is.na(TAUFR_VerbController)) %>%
    mutate(version = 1, ruleGroup = 2) %>% rename(TAU = TAUFR_VerbController),
  data %>% select(TAUIR_VerbController) %>% filter(!is.na(TAUIR_VerbController)) %>%
    mutate(version = 2, ruleGroup = 2) %>% rename(TAU = TAUIR_VerbController),
  data %>% select(TAUFR_CRUDNames) %>% filter(!is.na(TAUFR_CRUDNames)) %>%
    mutate(version = 1, ruleGroup = 3) %>% rename(TAU = TAUFR_CRUDNames),
  data %>% select(TAUIR_CRUDNames) %>% filter(!is.na(TAUIR_CRUDNames)) %>%
    mutate(version = 2, ruleGroup = 3) %>% rename(TAU = TAUIR_CRUDNames),
  data %>% select(TAUFR_PathHierarchy1) %>% filter(!is.na(TAUFR_PathHierarchy1)) %>%
    mutate(version = 1, ruleGroup = 4) %>% rename(TAU = TAUFR_PathHierarchy1),
  data %>% select(TAUIR_PathHierarchy1) %>% filter(!is.na(TAUIR_PathHierarchy1)) %>%
    mutate(version = 2, ruleGroup = 4) %>% rename(TAU = TAUIR_PathHierarchy1),
  data %>% select(TAUFR_PathHierarchy2) %>% filter(!is.na(TAUFR_PathHierarchy2)) %>%
    mutate(version = 1, ruleGroup = 5) %>% rename(TAU = TAUFR_PathHierarchy2),
  data %>% select(TAUIR_PathHierarchy2) %>% filter(!is.na(TAUIR_PathHierarchy2)) %>%
    mutate(version = 2, ruleGroup = 5) %>% rename(TAU = TAUIR_PathHierarchy2),
  data %>% select(TAUFR_PathHierarchy3) %>% filter(!is.na(TAUFR_PathHierarchy3)) %>%
    mutate(version = 1, ruleGroup = 6) %>% rename(TAU = TAUFR_PathHierarchy3),
  data %>% select(TAUIR_PathHierarchy3) %>% filter(!is.na(TAUIR_PathHierarchy3)) %>%
    mutate(version = 2, ruleGroup = 6) %>% rename(TAU = TAUIR_PathHierarchy3)
) %>%
  mutate(version = factor(version, levels = c(1, 2), labels = c("Rule", "Violation"))) %>%
  mutate(ruleGroup = factor(ruleGroup, levels = c(1:6), labels = c("#1: PluralNoun", "#2: VerbController", "#3: CRUDNames", "#4: PathHierarchy1", "#5: PathHierarchy2", "#6: PathHierarchy3")))

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
stat_summary(fun = "median", geom = "point", shape = 18, size = 7, color = "#ffa600d8") +
labs(x = "Treatment", y = "TAU") +
theme(
  text = element_text(size = 18, face = "bold", family = "sans"),
  axis.title = element_text(size = 18),
  axis.text.x = element_text(size = 16),
  axis.text.y = element_text(size = 14),
  legend.position = "none"
)

# rules NoTunnel, GETRetrieve, POSTCreate, NoRC200Error, RC401, and RC415
stripPlotData <- rbind(
  data %>% select(TAUFR_NoTunnel) %>% filter(!is.na(TAUFR_NoTunnel)) %>%
    mutate(version = 1, ruleGroup = 1) %>% rename(TAU = TAUFR_NoTunnel),
  data %>% select(TAUIR_NoTunnel) %>% filter(!is.na(TAUIR_NoTunnel)) %>%
    mutate(version = 2, ruleGroup = 1) %>% rename(TAU = TAUIR_NoTunnel),
  data %>% select(TAUFR_GETRetrieve) %>% filter(!is.na(TAUFR_GETRetrieve)) %>%
    mutate(version = 1, ruleGroup = 2) %>% rename(TAU = TAUFR_GETRetrieve),
  data %>% select(TAUIR_GETRetrieve) %>% filter(!is.na(TAUIR_GETRetrieve)) %>%
    mutate(version = 2, ruleGroup = 2) %>% rename(TAU = TAUIR_GETRetrieve),
  data %>% select(TAUFR_POSTCreate) %>% filter(!is.na(TAUFR_POSTCreate)) %>%
    mutate(version = 1, ruleGroup = 3) %>% rename(TAU = TAUFR_POSTCreate),
  data %>% select(TAUIR_POSTCreate) %>% filter(!is.na(TAUIR_POSTCreate)) %>%
    mutate(version = 2, ruleGroup = 3) %>% rename(TAU = TAUIR_POSTCreate),
  data %>% select(TAUFR_NoRC200Error) %>% filter(!is.na(TAUFR_NoRC200Error)) %>%
    mutate(version = 1, ruleGroup = 4) %>% rename(TAU = TAUFR_NoRC200Error),
  data %>% select(TAUIR_NoRC200Error) %>% filter(!is.na(TAUIR_NoRC200Error)) %>%
    mutate(version = 2, ruleGroup = 4) %>% rename(TAU = TAUIR_NoRC200Error),
  data %>% select(TAUFR_RC401) %>% filter(!is.na(TAUFR_RC401)) %>%
    mutate(version = 1, ruleGroup = 5) %>% rename(TAU = TAUFR_RC401),
  data %>% select(TAUIR_RC401) %>% filter(!is.na(TAUIR_RC401)) %>%
    mutate(version = 2, ruleGroup = 5) %>% rename(TAU = TAUIR_RC401),
  data %>% select(TAUFR_RC415) %>% filter(!is.na(TAUFR_RC415)) %>%
    mutate(version = 1, ruleGroup = 6) %>% rename(TAU = TAUFR_RC415),
  data %>% select(TAUIR_RC415) %>% filter(!is.na(TAUIR_RC415)) %>%
    mutate(version = 2, ruleGroup = 6) %>% rename(TAU = TAUIR_RC415)
) %>%
  mutate(version = factor(version, levels = c(1, 2), labels = c("Rule", "Violation"))) %>%
  mutate(ruleGroup = factor(ruleGroup, levels = c(1:6), labels = c("#7: NoTunnel", "#8: GETRetrieve", "#9: POSTCreate", "#10: NoRC200Error", "#11: RC401", "#12: RC415")))

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
stat_summary(fun = "median", geom = "point", shape = 18, size = 7, color = "#ffa600d8") +
labs(x = "Treatment", y = "TAU") +
theme(
  text = element_text(size = 16, face = "bold", family = "sans"),
  axis.title = element_text(size = 18),
  axis.text.x = element_text(size = 16),
  axis.text.y = element_text(size = 14),
  legend.position = "none"
)

# start hypothesis testing
# due to multiple hypotheses, we will use the Holm-Bonferroni correction to adjust the computed p-values; the confidence level is therefore set to 0.05 here
confLevel <- 0.05

# calculate Wilcoxon–Mann–Whitney test
# standard implementation from the `stats` package (asymptotic approximation with ties)

# for individual rules
testResults <- data.frame()
for (var in ruleNames) {
  varTAUFR <- paste("TAUFR", var, sep = "_")
  varTAUIR <- paste("TAUIR", var, sep = "_")
  w <- wilcox.test(
    x = data[[varTAUFR]],
    y = data[[varTAUIR]],
    alternative = "greater",
    conf.level = confLevel
  )
  # calculate the effect size with Cohens d
  d <- cohens_d(data[[varTAUFR]], data[[varTAUIR]])

  # create results data frame
  rule <- c(var)
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
  x = combinedDf$FR_TAU,
  y = combinedDf$IR_TAU,
  alternative = "greater",
  conf.level = confLevel
)
d <- cohens_d(combinedDf$FR_TAU, combinedDf$IR_TAU)
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
  filter(rule != "All rules combined" & rule != "PathHierarchy3")

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

for (var in ruleNames) {
  varTAUFR <- as.name(paste("TAUFR", var, sep = "_"))
  varTAUIR <- as.name(paste("TAUIR", var, sep = "_"))
  varFR <- as.name(paste(var, "FR", sep = ""))
  varIR <- as.name(paste(var, "IR", sep = ""))
  varFR_rating <- as.name(paste(var, "FR_rating", sep = ""))
  varIR_rating <- as.name(paste(var, "IR_rating", sep = ""))
  descriptiveStats <- rbind(
    descriptiveStats,
    data %>% summarise(
      rule = var,
      median_rating_FR := median({{ varFR_rating }}, na.rm = TRUE),
      median_rating_IR := median({{ varIR_rating }}, na.rm = TRUE),
      mean_rating_FR := round(mean({{ varFR_rating }}, na.rm = TRUE), 2),
      mean_rating_IR := round(mean({{ varIR_rating }}, na.rm = TRUE), 2),
      mean_TAU_FR := mean({{ varTAUFR }}, na.rm = TRUE),
      mean_TAU_IR := mean({{ varTAUIR }}, na.rm = TRUE),
      correctPercent_FR := scales::percent(sum({{ varFR }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varFR }})) %>% nrow())),
      correctPercent_IR := scales::percent(sum({{ varIR }}, na.rm = TRUE) / (data %>% filter(!is.na({{ varIR }})) %>% nrow()))
    )
  )
}

print(descriptiveStats)

# calculate more detailed descriptive stats per individual rule (min, max, var)
descriptiveStatsDetails <- data.frame()

for (var in ruleNames) {
  varFR_rating <- as.name(paste(var, "FR_rating", sep = ""))
  varIR_rating <- as.name(paste(var, "IR_rating", sep = ""))

  descriptiveStatsDetails <- rbind(
    descriptiveStatsDetails,
    data %>% summarise(
      rule = var,
      min_rating_FR := min({{ varFR_rating }}, na.rm = TRUE),
      min_rating_IR := min({{ varIR_rating }}, na.rm = TRUE),
      max_rating_FR := max({{ varFR_rating }}, na.rm = TRUE),
      max_rating_IR := max({{ varIR_rating }}, na.rm = TRUE),
      var_rating_FR := var({{ varFR_rating }}, na.rm = TRUE),
      var_rating_IR := var({{ varIR_rating }}, na.rm = TRUE)
    )
  )
}

print(descriptiveStatsDetails)

# create custom likert plots for perceived understandability ratings
ratings <- data.frame()
for (var in ruleNames) {
  var <- as.name(var)
  varRatingFR <- as.name(paste(var, "FR_rating", sep = ""))
  varRatingIR <- as.name(paste(var, "IR_rating", sep = ""))
  FR1 <- data %>% filter({{ varRatingFR }} == 1) %>% nrow() * -1
  FR2 <- data %>% filter({{ varRatingFR }} == 2) %>% nrow() * -1
  IR1 <- data %>% filter({{ varRatingIR }} == 1) %>% nrow()
  IR2 <- data %>% filter({{ varRatingIR }} == 2) %>% nrow()

  ratings <- rbind(ratings,
    data.frame(
      rule = as.character(var),
      countFR1 = FR1,
      countFR2 = FR2,
      countIR2 = IR2,
      countIR1 = IR1
    )
  )
}

print(ratings)

# melt the data frame into long format and create factor for ratings
ratings_long <- reshape2::melt(ratings, id.vars = "rule")
ratings_long$variable <- factor(
  ratings_long$variable,
  levels = c("countFR1", "countFR2", "countIR1", "countIR2"),
  labels = c("Very easy (rule)", "Easy (rule)", "Very easy (violation)", "Easy (violation)")
)

print(ratings_long)

print(ruleNames)

# order according to categories
ratings_long <- ratings_long %>%
  arrange(factor(rule, levels = rev(ruleNames))) %>%
  mutate(index = row_number())


print(ratings_long)

# create break values to avoid negative numbers
break_values <- append(pretty(ratings_long$value), c(30, 40, 50))

print(break_values)

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
for (var in ruleNames) {
  varRatingFR <- paste(var, "FR_rating", sep = "")
  varRatingIR <- paste(var, "IR_rating", sep = "")
  w <- wilcox.test(
    x = data[[varRatingIR]],
    y = data[[varRatingFR]],
    alternative = "greater",
    conf.level = confLevel
  )
  # calculate the effect size with Cohens d
  d <- cohens_d(data[[varRatingIR]], data[[varRatingFR]])

  # create results data frame
  rule <- c(var)
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

print(combinedDf)
# for all rules combined
w <- wilcox.test(
  x = combinedDf$IR_rating,
  y = combinedDf$FR_rating,
  alternative = "greater",
  conf.level = confLevel
)
d <- cohens_d(combinedDf$IR_rating, combinedDf$FR_rating)
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
  filter(rule != "All rules combined" & rule != "PathHierarchy3" &
  rule != "VerbController" & rule != "RC415")

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
correlationResults <- data.frame()
corrMthd <- "kendall"

# for each individual rule
for (var in ruleNames) {
  varRatingFR <- paste(var, "FR_rating", sep = "")
  varRatingIR <- paste(var, "IR_rating", sep = "")
  varTAUFR <- paste("TAUFR", var, sep = "_")
  varTAUIR <- paste("TAUIR", var, sep = "_")

  corFR <- cor.test(
    data[[varRatingFR]],
    data[[varTAUFR]],
    method = corrMthd,
    alternative = "less",
    conf.level = confLevel
  )
  corIR <- cor.test(
    data[[varRatingIR]],
    data[[varTAUIR]],
    method = corrMthd,
    alternative = "less",
    conf.level = confLevel
  )
  correlationResults <- rbind(correlationResults,
    data.frame(
      rule = var,
      FR_correlation = corFR$estimate,
      FR_p.value = corFR$p.value,
      IR_correlation = corIR$estimate,
      IR_p.value = corIR$p.value
    ),
    make.row.names = FALSE
  )
}

print(correlationResults)

# adjust p-values with Holm-Bonferroni and format them
correlationResults <- correlationResults %>%
  mutate(FR_p.value = format.pval(
      p.adjust(FR_p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  ) %>%
  mutate(IR_p.value = format.pval(
      p.adjust(IR_p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  )
print(correlationResults)

# for all rules combined
corFR <- cor.test(
  combinedDf$FR_rating,
  combinedDf$FR_TAU,
  method = corrMthd,
  alternative = "less",
  conf.level = confLevel
)
corIR <- cor.test(
  combinedDf$IR_rating,
  combinedDf$IR_TAU,
  method = corrMthd,
  alternative = "less",
  conf.level = confLevel
)
correlationResults <- rbind(correlationResults,
  data.frame(
    rule = "All rules combined",
    FR_correlation = corFR$estimate,
    FR_p.value = format.pval(corFR$p.value, digits = 4, eps = 0.001),
    IR_correlation = corIR$estimate,
    IR_p.value = format.pval(corIR$p.value, digits = 4, eps = 0.001)
  ),
  make.row.names = FALSE
)

print(correlationResults)

# regression results for each individual rule
df <- data.frame()

for (var in ruleNames) {
  varRatingFR <- paste(var, "FR_rating", sep = "")
  varRatingIR <- paste(var, "IR_rating", sep = "")
  varTAUFR <- paste("TAUFR", var, sep = "_")
  varTAUIR <- paste("TAUIR", var, sep = "_")

  resFR <- lm(
    as.formula(paste(varTAUFR, "~", varRatingFR)),
    data = data
  )
  resIR <- lm(
    as.formula(paste(varTAUIR, "~", varRatingIR)),
    data = data
  )
  df <- rbind(df,
    data.frame(
      rule = var,
      FR_adjustedR2 = summary(resFR)$adj.r.squared,
      FR_p.value = format.pval(summary(resFR)$coefficients[8], digits = 4, eps = 0.001),
      IR_adjustedR2 = summary(resIR)$adj.r.squared,
      IR_p.value = format.pval(summary(resIR)$coefficients[8], digits = 4, eps = 0.001)
    ),
    make.row.names = FALSE
  )
}

print(df)

df %>% arrange(IR_adjustedR2) %>%
  print

# visualize adjusted R-squared values for violation
barplotData <- df %>%
  select(rule, IR_adjustedR2)

print(barplotData)

# use ggplot to print the bar chart
ggplot(barplotData, aes(x = reorder(rule, IR_adjustedR2), y = IR_adjustedR2)) +
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
    label = sprintf("%.2f", round(IR_adjustedR2, 2)),
    # fix label placement for negative numbers
    y = ifelse(IR_adjustedR2 > 0, IR_adjustedR2 + 0.001, IR_adjustedR2 - 0.025)
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
# Calculations for RQ3 (How does REST related experience influence the results of RQ1 and RQ2)
#########################################################################################################

# aggregate mean values for TAU, perceived understandability, correctness, and time (needed for RQ3)
correlationData <- data %>%
  rowwise() %>%
  mutate(
    mean_TAU_FR = ifelse(
      group_id == 1,
      mean(c(TAUFR_PluralNoun, TAUFR_PathHierarchy2, TAUFR_PathHierarchy3, TAUFR_CRUDNames, TAUFR_NoTunnel, TAUFR_RC401), na.rm = TRUE),
      mean(c(TAUFR_VerbController, TAUFR_GETRetrieve, TAUFR_POSTCreate, TAUFR_RC415, TAUFR_NoRC200Error, TAUFR_PathHierarchy1), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_TAU_IR = ifelse(
      group_id == 1,
      mean(c(TAUIR_VerbController, TAUIR_GETRetrieve, TAUIR_POSTCreate, TAUIR_RC415, TAUIR_NoRC200Error, TAUIR_PathHierarchy1), na.rm = TRUE),
      mean(c(TAUIR_PluralNoun, TAUIR_PathHierarchy2, TAUIR_PathHierarchy3, TAUIR_CRUDNames, TAUIR_NoTunnel, TAUIR_RC401), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_perceivedDifficulty_FR = ifelse(group_id == 1,
      mean(c(PluralNounFR_rating, PathHierarchy2FR_rating, PathHierarchy3FR_rating, CRUDNamesFR_rating, NoTunnelFR_rating, RC401FR_rating), na.rm = TRUE),
      mean(c(VerbControllerFR_rating, GETRetrieveFR_rating, POSTCreateFR_rating, RC415FR_rating, NoRC200ErrorFR_rating, PathHierarchy1FR_rating), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_perceivedDifficulty_IR = ifelse(group_id == 1,
      mean(c(VerbControllerIR_rating, GETRetrieveIR_rating, POSTCreateIR_rating, RC415IR_rating, NoRC200ErrorIR_rating, PathHierarchy1IR_rating), na.rm = TRUE),
      mean(c(PluralNounIR_rating, PathHierarchy2IR_rating, PathHierarchy3IR_rating, CRUDNamesIR_rating, NoTunnelIR_rating, RC401IR_rating), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Time_FR = ifelse(group_id == 1,
      mean(c(PluralNounFRTime, PathHierarchy2FRTime, PathHierarchy3FRTime, CRUDNamesFRTime, NoTunnelFRTime, RC401FRTime), na.rm = TRUE),
      mean(c(VerbControllerFRTime, GETRetrieveFRTime, POSTCreateFRTime, RC415FRTime, NoRC200ErrorFRTime, PathHierarchy1FRTime), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Time_IR = ifelse(group_id == 1,
      mean(c(VerbControllerIRTime, GETRetrieveIRTime, POSTCreateIRTime, RC415IRTime, NoRC200ErrorIRTime, PathHierarchy1IRTime), na.rm = TRUE),
      mean(c(PluralNounIRTime, PathHierarchy2IRTime, PathHierarchy3IRTime, CRUDNamesIRTime, NoTunnelIRTime, RC401IRTime), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Corr_FR = ifelse(group_id == 1,
      mean(c(PluralNounFR, PathHierarchy2FR, PathHierarchy3FR, CRUDNamesFR, NoTunnelFR, RC401FR), na.rm = TRUE),
      mean(c(VerbControllerFR, GETRetrieveFR, POSTCreateFR, RC415FR, NoRC200ErrorFR, PathHierarchy1FR), na.rm = TRUE)
    )
  ) %>%
  mutate(
    mean_Corr_IR = ifelse(group_id == 1,
      mean(c(VerbControllerIR, GETRetrieveIR, POSTCreateIR, RC415IR, NoRC200ErrorIR, PathHierarchy1IR), na.rm = TRUE),
      mean(c(PluralNounIR, PathHierarchy2IR, PathHierarchy3IR, CRUDNamesIR, NoTunnelIR, RC401IR), na.rm = TRUE)
    )
  )

print(correlationData)

# Correlation matrix for exploration
# rcorr does not support kendalls TAU
# "pearson" for linear correlation of continuous variables
# "spearman" for rank-based monotonic correlation (with ordinal variables)
corrMthd <- "spearman"
corrMatrix <-
  correlationData %>%
  select(
    starts_with("mean_"),
    starts_with("is_"),
    YearsOfExperience,
    RichardsonMaturity,
    MaturityLevel
  ) %>%
  as.matrix() %>%
  rcorr(type = corrMthd)

# plot a correlation matrix
corrplot(corrMatrix$r, p.mat = corrMatrix$P, method = "circle", type = "lower")

# caculate separate correlations
corrMthd <- "kendall"
df <- data.frame()
# change to "mean_TAU_FR", "mean_TAU_IR", "mean_perceivedDifficulty_FR", or "mean_perceivedDifficulty_IR"
dependent <- "mean_TAU_FR"
demographics <- c("is_Student", "is_Academia", "is_Germany", "YearsOfExperience", "RichardsonMaturity", "MaturityLevel")

for (d in demographics) {
  res <- cor.test(
      correlationData[[dependent]],
      correlationData[[d]],
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

print(df)

# adjust p-values with Holm-Bonferroni and format them
df %>%
  mutate(p.value = format.pval(
      p.adjust(p.value, method = "holm"),
      digits = 4, eps = 0.001
    )
  ) %>%
  arrange(p.value) %>%
  
print(df)

# create 2 linear regression models for predicting TAU (one for following rules and one for violating rules)
# LM for rule:
lrFR <- lm(
  mean_TAU_FR ~
    is_Student
    + is_Academia
    + is_Germany
    + YearsOfExperience
    + MaturityLevel,
  data = correlationData
)
summary(lrFR)

# LM for violation:
lrIR <- lm(
  mean_TAU_IR ~
    is_Student
    + is_Academia
    + is_Germany
    + YearsOfExperience
    + MaturityLevel,
  data = correlationData
)
summary(lrIR)
