from fastapi import FastAPI
from sklearn.linear_model import LinearRegression

app = FastAPI()

@app.get("/forecast")

def forecast():

 data=[10,12,13,15,18,20]

 X=[[i] for i in range(len(data))]

 model=LinearRegression()
 model.fit(X,data)

 prediction=model.predict([[7]])

 return {"predicted_sales": float(prediction)}
