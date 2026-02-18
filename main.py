from fastapi import FastAPI
from utilis.db import Base,engine
from router import userRouter,productRouter,cartRouter
from model import userModel,productModel,cartModel
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(userRouter.router)
app.include_router(productRouter.router)
app.include_router(cartRouter.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]   
)