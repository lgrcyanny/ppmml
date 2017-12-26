library("randomForest")
rf = randomForest(Species ~ ., data = iris)
saveRDS(rf, "./rf.rds")
