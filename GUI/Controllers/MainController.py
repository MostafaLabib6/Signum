import numpy as np
import model.model_functions as NN
import matplotlib.pyplot as plt
import seaborn as sns
from dependency_injector.wiring import Provide, inject
import Services.DataPreProcessingService as dpp
@inject
class MainController:

# instance attributes
   def __init__(self):
        self.service = dpp.DataPreProcessingService()
        self.data= self.service.SharedPreProcessing()

    # instance method
   def classFillter(self, class1:str,class2:str):
         self.c1=class1
         self.c2=class2
         self.data=self.service.classFillter(class1=class1,class2=class2) 
    
   def FeatureFillter(self, feat1:str,feat2:str):
     self.f1=feat1
     self.f2=feat2
     self.y,self.ytest,self.train,self.test =self.service.FeatureFillter(feat1=feat1,feat2=feat2)


   def trainModel(self,learning_rate=0.01,bais=False,epochs=2000):
       self.w,self.b= NN.model(X_train=self.train,learning_rate=learning_rate,withBias=bais,num_iterations=epochs,Y_train= self.y,X_test=self.test,Y_test=self.ytest)
        
   def testModel(self):
     acc,Cmatrx=NN.predict(self.test,self.w,self.b,self.ytest)
     self.test = self.test.to_numpy()
     index=np.argmin(self.test[0])
     self.test[0][index]=self.b
     sns.scatterplot(data=self.data, x=self.f1, y=self.f2, hue='species')
     plt.plot(self.test[0], ((-self.w[0] / self.w[1]) * self.test[0] - self.b / self.w[1]), color='k')
     plt.show()
     fig, ax = plt.subplots(figsize=(7.5, 7.5))
     ax.matshow(Cmatrx, cmap=plt.cm.Blues, alpha=0.3)
     for i in range(Cmatrx.shape[0]):
      for j in range(Cmatrx.shape[1]):
        ax.text(x=j, y=i,s=Cmatrx[i, j], va='center', ha='center', size='xx-large')
    
     plt.xlabel('Predictions', fontsize=18)
     plt.ylabel('Actuals', fontsize=18)
     plt.title('Confusion Matrix', fontsize=18)
     fig.show()

     return acc
   def showGraphs(self):
        NN.plots(self.data)