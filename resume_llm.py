import os
# libraries for model
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import LLMChain

# libraries for document loading
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader

# libraries for pydantic functions
from typing import List
from typing import Optional
from pydantic import BaseModel, Field
from langchain.llms import OpenLLM


def connect_llm_model(openai_key):
    openai_model_name = "gpt-3.5-turbo" # can change model name here
    llm_kwargs = dict(
    model_name=openai_model_name,
    openai_api_key = openai_key,
    temperature = 0.3,
    model_kwargs=dict(
        frequency_penalty=0.1
        ),
    )
    chat_model = ChatOpenAI(**llm_kwargs)
    return chat_model

def file_reader(file_name):
    root, file_extension = os.path.splitext(file_name.lower())
        
    if file_extension == '.pdf':
        loader = PyPDFLoader(file_name)
        pages = loader.load_and_split()
        extracted_text = "\n".join([page.page_content for page in pages])
    elif file_extension == '.docx':
        # Assuming you have a read_text_from_docx function
        loader = Docx2txtLoader(file_name)
        pages = loader.load_and_split()
        extracted_text = "\n".join([page.page_content for page in pages])
    elif file_extension == '.txt':
        loader = TextLoader(file_name)
        pages = loader.load()
        extracted_text = "\n".join([page.page_content for page in pages])
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    return extracted_text

# Pydantic class defining the extraction of job-related information for an output parser
class Job_Description(BaseModel):
    """Description of a job posting"""

    company: str = Field(
        ..., description="Name of the company that has the job opening"
    )
    job_title: str = Field(..., description="Job title")
    team: str = Field(
        ...,
        description="Name of the team within the company. Team name should be null if it's not known.",
    )
    job_summary: str = Field(
        ..., description="Brief summary of the job, not exceeding 100 words"
    )
    salary: str = Field(
        ...,
        description="Salary amount or range. Salary should be null if it's not known.",
    )
    duties: List[str] = Field(
        ...,
        description="The role, responsibilities and duties of the job as an itemized list, not exceeding 500 words",
    )
    qualifications: List[str] = Field(
        ...,
        description="The qualifications, skills, and experience required for the job as an itemized list, not exceeding 500 words",
    )

# Pydantic class that defines a list of skills in the job posting
class Job_Skills(BaseModel):
    """Skills from a job posting"""

    technical_skills: List[str] = Field(
        ...,
        description="An itemized list of technical skills, including programming languages, technologies, and tools.",
    )
    non_technical_skills: List[str] = Field(
        ...,
        description="An itemized list of non-technical Soft skills.",
    )

# Pydantic class that defines a list of skills in the resume
class Resume_Skills(BaseModel):
    technical_skills: List[str] = Field(
        ...,
        description="An individual itemized list of technical skills Examples: Python, MS Office etc",
    )
    non_technical_skills: List[str] = Field(
        ...,
        description="An individual itemized list of non-technical skills like soft skills",
    )

# Pydantic class that defines a format of resume parser
class Resume_Format(BaseModel):
    """Format of resume"""
    Basics: str = Field(
        ..., description = " The basics of  the for given user resume input."
    )
    Introduction: str = Field(
        ..., description = " write only 1 line introduction for the introduction section for given user resume input."
    )
    Work_Experiences: str = Field(
        ..., description = " The experiece of the candidates with job, duration and description of work done like xyz company from 09-2022 to 08-2023 performed work on spark and databases"
    )
    Education: str = Field(
        ..., description = " The education of the candidates with university, duration and description of work done like xyx university from 08-2013 to 07-2018 studied this courses"
    )
    Awards: Optional[str] = Field(
        ..., description = " The awards are the achievments and honours of the candidates. If the resume don't have the award no need to add this to resume"
    )
    Projects: str = Field(
        ..., description = " The projects section of contains the project, duration and roles and responsibilities of the candidate like xyz project from 05-2019 to 04-2020 worked on backend etc"
    )
    Skills: List[str] = Field(
        ...,
        description=" An itemized list of technical skills and non-technical Soft skills of the user",
    )

# Pydantic class defining the format of improvements
class Resume_Improvements(BaseModel):
    improvements: List[str] = Field(
        ..., description="List of suggestions for improvement"
    )

