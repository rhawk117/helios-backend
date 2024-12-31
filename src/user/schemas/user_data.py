# # src/schemas/user_data.py

# from pydantic import BaseModel, Field, constr, model_validator
# from typing import Optional
# from datetime import datetime


# class UserDataValidate:

#     MAX_GRAD_YEAR = 2050

#     @staticmethod
#     def check_grad_year(grad_year: int) -> None:
#         if grad_year > UserDataValidate.MAX_GRAD_YEAR:
#             raise ValueError("Graduation year must be less than 2050.")

#     @staticmethod
#     def check_enroll_year(enroll_year: int) -> None:
#         if enroll_year > datetime.now().year:
#             raise ValueError("Enrollment year must be in the past.")

#     @staticmethod
#     def check_tenure_total(grad_year: int, enroll_year: int) -> None:
#         if (grad_year - enroll_year) < 0:
#             raise ValueError("Graduation year must be after enrollment year.")

#     @staticmethod
#     def check_user_data(model) -> None:
#         if model.graduation_year and model.enrollment_year:
#             UserDataValidate.check_tenure_total(
#                 model.graduation_year, model.enrollment_year
#             )
#         if model.graduation_year:
#             UserDataValidate.check_grad_year(model.graduation_year)
#         if model.enrollment_year:
#             UserDataValidate.check_enroll_year(model.enrollment_year)


# class UserDataCreate(BaseModel):
#     enrollment_year: int
#     graduation_year: int

#     major: str = Field(..., min_length=3, max_length=100)
#     minor: Optional[str] = Field(None, min_length=3, max_length=100)
#     concentration: Optional[str] = Field(None, min_length=3, max_length=100)

#     @model_validator(mode='after')
#     def check_user_data(cls, model):
#         UserDataValidate.check_user_data(model)
#         return model


# class UserDataUpdate(BaseModel):
#     enrollment_year: Optional[int]
#     graduation_year: Optional[int]

#     major: Optional[str] = Field(None, min_length=3, max_length=100)
#     minor: Optional[str] = Field(None, min_length=3, max_length=100)
#     concentration: Optional[str] = Field(None, min_length=3, max_length=100)

#     @model_validator(mode='after')
#     def check_user_data_update(cls, model):
#         UserDataValidate.check_user_data(model)
#         return model


# class UserDataResponse(BaseModel):
#     id: str
#     enrollment_year: int
#     graduation_year: int
#     major: str
#     minor: Optional[str]
#     concentration: Optional[str]

#     class Config:
#         orm_mode = True
