setwd('/Users/Krishno Dey/Documents/Linguistic/Result-Summary/Mosaic')
list.files()

library(vcd)
library(gdata)
library(readxl)

par(mar=c(0,0,0,0))

mycolors<-c("white","black")

AP <- read_xlsx("Data.xlsx", sheet = 1)
P <- read_xlsx("Data.xlsx", sheet=2)


print(P)
results = array(1, dim=c(10,12,2))
print(results)

dimnames(results)<-
  list(
    c("Amorphous End-point", "Non-standard End-point", "CRUDy End-point", "Non-descriptive End-point", "UnversionedURI", "Pluralized Nodes", "Contextless Resources", "Non-hierarchical Nodes", "Non-pertinent Documentation","Inconsistent Documentation" ), 
    colnames(P[2:12]), 
    c("P", "AP")
  )

print(colnames(P[2:12]))
print(dimnames(results))
