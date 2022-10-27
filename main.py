import os


########## LECTURES ##########
#LECTURE = '01_basic_api'
#LECTURE = '02_basic_api_postgres'
# LECTURE = '03_basic_api_orm'
# LECTURE = '04_basic_api_user'
# LECTURE = '05_basic_api_relationships'
LECTURE = '06_basic_api_voting'

# Hauptfunktion
if __name__ == '__main__':
    os.system('cls')
    print(LECTURE)

    if LECTURE == '01_basic_api':
        os.system('uvicorn app.basic_api:app --reload')

    elif LECTURE == '02_basic_api_postgres':
        os.system('uvicorn app.basic_api_postgres:app --reload')

    elif LECTURE == '03_basic_api_orm':
        os.system('uvicorn app.basic_api_orm:app --reload')

    elif LECTURE == '04_basic_api_user':
        os.system('uvicorn app.basic_api_user:app --reload')
    
    elif LECTURE == '05_basic_api_relationships':
        os.system('uvicorn app.basic_api_relationships:app --reload')

    elif LECTURE == '06_basic_api_voting':
        os.system('uvicorn app.basic_api_voting:app --reload')

    else:
        print(f'No lecture found!')


