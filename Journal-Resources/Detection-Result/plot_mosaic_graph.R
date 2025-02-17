setwd('/Users/Krishno Dey/Documents/Linguistic/Result-Summary/Mosaic')
list.files()

library(vcd)
library(gdata)
library(readxl)

par(mar=c(0,0,0,0))

mycolors<-c("white","black")

AP <- read_xlsx("Data-Mosaic.xlsx", sheet = 1)
P <- read_xlsx("Data-Mosaic.xlsx", sheet=2)

print(AP)

results = array(1, dim=c(14,31,2))

dimnames(results)<-
  list(
    c("Amorphous", "Contextless", "CRUDy", "InconsistentDoc", "NonDescriptive", "NonHierarchical", "NonPertinent", "NonStandard", "Pluralized", "Unversioned", "Tunneling","InconArchetype", "Ambiguity",  "Flat"), 
    colnames(P[2:32]), 
    c("P", "AP")
  )

for (i in 1:14) 
{
  for (j in 2:32)
  {
    #print(AP[i,j][1])
    results[i,j-1,2]<-as.numeric(AP[i,j])
    results[i,j-1,1]<-as.numeric(P[i,j])
  }
}

#print(results)

pdf("GraphQL.pdf", width = 10, height = 16)
mosaicplot(results, shade=FALSE, dir = "v", off=10, cex.axis=.8,color = mycolors, las=2, main=NULL)
dev.off()


AP <- read_xlsx("Data-Mosaic.xlsx", sheet = 3)
P <- read_xlsx("Data-Mosaic.xlsx", sheet=4)


results = array(1, dim=c(14,37,2))

print(results)

dimnames(results)<-
  list(
    c("Amorphous", "Contextless", "CRUDy", "InconsistentDoc", "NonDescriptive", "NonHierarchical", "NonPertinent", "NonStandard", "Pluralized", "Unversioned", "Tunneling","InconArchetype", "Ambiguity",  "Flat"), 
    colnames(P[2:38]), 
    c("P", "AP")
  )

for (i in 1:14) 
{
  for (j in 2:38)
  {
    #print(AP[i,j][1])
    results[i,j-1,2]<-as.numeric(AP[i,j])
    results[i,j-1,1]<-as.numeric(P[i,j])
  }
}  

  
pdf("REST.pdf", width = 10, height = 15)
mosaicplot(results,shade=FALSE, dir = "v", off=10, cex.axis=.8,color = mycolors, las=2, main=NULL)
dev.off()

