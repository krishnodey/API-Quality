setwd('/Users/Krishno Dey/Documents/Linguistic/Result-Summary/Mosaic')
list.files()

library(vcd)
library(gdata)
library(readxl)

par(mar=c(0,0,0,0))

mycolors<-c("white","black")

AP <- read_xlsx("Data.xlsx", sheet = 1)
P <- read_xlsx("Data.xlsx", sheet=2)


results = array(1, dim=c(10,12,2))

dimnames(results)<-
  list(
    c("Amorphous End-point", "Non-standard End-point", "CRUDy End-point", "Non-descriptive End-point", "UnversionedURI", "Pluralized Nodes", "Contextless Resources", "Non-hierarchical Nodes", "Non-pertinent Documentation","Inconsistent Documentation" ), 
    colnames(P[2:13]), 
    c("P", "AP")
  )

for (i in 1:10) 
{
  for (j in 2:13)
  {
    print(AP[i,j][1])
    results[i,j-1,2]<-as.numeric(AP[i,j])
    results[i,j-1,1]<-as.numeric(P[i,j])
  }
}
pdf("GraphQL.pdf", width = 9)
mosaicplot(results,shade=FALSE, dir = "v", off=10, cex.axis=.8,color = mycolors, las=2, main=NULL)
dev.off()


AP <- read_xlsx("Data.xlsx", sheet = 3)
P <- read_xlsx("Data.xlsx", sheet=4)


results = array(1, dim=c(10,21,2))

dimnames(results)<-
  list(
    c("Amorphous End-point", "Non-standard End-point", "CRUDy End-point", "Non-descriptive End-point", "UnversionedURI", "Pluralized Nodes", "Contextless Resources", "Non-hierarchical Nodes", "Non-pertinent Documentation","Inconsistent Documentation" ), 
    colnames(P[2:22]), 
    c("P", "AP")
  )

for (i in 1:10) 
{
  for (j in 2:22)
  {
    print(AP[i,j][1])
    results[i,j-1,2]<-as.numeric(AP[i,j])
    results[i,j-1,1]<-as.numeric(P[i,j])
  }
}
pdf("REST.pdf", width = 9)
mosaicplot(results,shade=FALSE, dir = "v", off=10, cex.axis=.8,color = mycolors, las=2, main=NULL)
dev.off()

