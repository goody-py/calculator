from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, PositiveInt
from fastapi.middleware.cors import CORSMiddleware


class StrictPositiveInt(PositiveInt):
    strict = True


class CalculationRequestModel(BaseModel):
    number1: StrictPositiveInt
    number2: StrictPositiveInt


class ResultResponseModel(BaseModel):
    result: StrictPositiveInt


calculator = FastAPI()
calculator.mount('/static', StaticFiles(directory="static"), name='static')


origins = ['*']


calculator.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@calculator.get('/')
def index_page():
    return FileResponse('index.html')


@calculator.post('/calc')
def process_calculation(number_object: CalculationRequestModel):
    number_sum = number_object.number1 + number_object.number2
    return ResultResponseModel(result=number_sum)


if __name__ == '__main__':
    # Use it for debugging
    import uvicorn
    uvicorn.run(calculator, host='0.0.0.0', port=8000)
