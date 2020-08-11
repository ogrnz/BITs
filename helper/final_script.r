library("ggplot2")
library("ggpubr")
library("stargazer")
library("gridExtra")

data <- read.csv("data.csv", header=TRUE)

sfi <- data$MaxSFI
democ <- data$MaxDemoc
gdp <- data$MaxGDPCurrent
diff <- data$DiffFlowsTot
score <- data$scor
year <- data$Year.of.signature


lm <- lm(score ~ diff, data=data)
lm_democ <- lm(score ~ diff + democ, data=data)
lm_sfi <- lm(score ~ diff + sfi, data=data)
lm_gdp <- lm(score ~ diff + gdp, data=data)
lm_tot_controls <- lm(score ~ diff + democ + sfi + gdp, data=data)



box<-boxplot(score, ylab="Regulatory score", col="#196b3b")
boxout<-boxplot(score, ylab="Regulatory score", outline=FALSE, col="#196b3b")
time_score <- ggplot(data, aes(x=year, y=score)) + 
  geom_point(color="#196b3b")+ ggtitle("Regulatory score over time") +labs(x="Years", y="Regulatory score")

par(mfrow=c(3,2))

plot(diff, score, ylab="Regulatory score", xlab="Dependency and integration", main="Model 1")
abline(lm, col="blue")

plot(diff, score, ylab="Regulatory score", xlab="Dependency and integration", main="Model 2")
abline(lm_democ, col="red")

plot(diff, score, ylab="Regulatory score", xlab="Dependency and integration", main="Model 3")
abline(lm_sfi, col="orange")

plot(diff, score,ylab="Regulatory score", xlab="Dependency and integration", main="Model 4")
abline(lm_gdp, col="pink")

plot(diff, score,ylab="Regulatory score", xlab="Dependency and integration",  main="Model 5")
abline(lm_tot_controls, col="#196b3b")

stargazer(type="html", out="regressions.html", style="all", lm, lm_democ, lm_sfi, lm_gdp, lm_tot_controls, title="Results", align=TRUE)

#Get subset dataframes
usa <- subset(data, data$ISO.Party1=='USA' | data$ISO.Party2=='USA')
jpn <- subset(data, data$ISO.Party1=='JPN' | data$ISO.Party2=='JPN')
che <- subset(data, data$ISO.Party1=='CHE' | data$ISO.Party2=='CHE')

chn <- subset(data, data$ISO.Party1=='CHN' | data$ISO.Party2=='CHN')
bra <- subset(data, data$ISO.Party1=='BRA' | data$ISO.Party2=='BRA')

zwe <- subset(data, data$ISO.Party1=='ZWE' | data$ISO.Party2=='ZWE')
cd <- subset(data, data$ISO.Party1=='CD' | data$ISO.Party2=='CD')

time_usa <- ggplot(data=usa, aes(x=usa$Year.of.signature, y=usa$score))+ggtitle("USA")+ labs(x="Year", y="Regulatory score") +
  theme(plot.title = element_text(hjust = 0.5))+geom_point(color = "#196b3b", size = 2)
time_jpn<- ggplot(data=jpn, aes(x=jpn$Year.of.signature, y=jpn$score))+ggtitle("Japan") + labs(x="Year", y="Regulatory score")+
  theme(plot.title = element_text(hjust = 0.5)) + geom_point(color = "#196b3b", size = 2)
#time_che<- ggplot(data=che, aes(x=che$Year.of.signature, y=che$score)) + geom_point(color = "blue", size = 2)

time_chn <- ggplot(data=chn, aes(x=chn$Year.of.signature, y=chn$score))+ggtitle("China") + labs(x="Year", y="Regulatory score") +
  theme(plot.title = element_text(hjust = 0.5))+ geom_point(color = "#196b3b", size = 2)
time_bra <- ggplot(data=bra, aes(x=bra$Year.of.signature, y=bra$score))+ggtitle("Brazil") + labs(x="Year", y="Regulatory score")+
  theme(plot.title = element_text(hjust = 0.5)) + geom_point(color = "#196b3b", size = 2)

time_zwe <- ggplot(data=zwe, aes(x=zwe$Year.of.signature, y=zwe$score))+ggtitle("Zimbabwe") +
  theme(plot.title = element_text(hjust = 0.5))+ labs(x="Year", y="Regulatory score") + geom_point(color = "#196b3b", size = 2)
time_cd <- ggplot(data=cd, aes(x=cd$Year.of.signature, y=cd$score))+ggtitle("Dem. Rep. of Congo")+
  theme(plot.title = element_text(hjust = 0.5)) + labs(x="Year", y="Regulatory score") + geom_point(color = "#196b3b", size = 2)

grid.arrange(time_usa, time_jpn, time_chn, time_bra, time_zwe, time_cd, nrow=3)
