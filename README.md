# EcoPositive Bristol (Django REST API)

[EcoPositive Bristol](https://tastesensation-pp4-54d01fbc1628.herokuapp.com/) is a one stop directory championing Bristol’s eco-conscious and socially responsible businesses.

Users are invited to sign up to endorse the companies that they support and comment on listed businesses so that other visitors to the site can see which businesses are popular.

![Placeholder mock up on multiple devices](placeholder image)

### Design Process

***Wireframes***

- Initial Wireframe designs were used to plan out the layout for the Company List and Company Detail pages

![Directory Listing Wireframe Design](docs/readme-images/home-page-laptop.png)

![Company Detail Wireframe Design](docs/readme-images/company-details-laptop.png)

***Models***

- The next step was to plan and devise an ERD for each of my database models and a schema to map out and understand the relationships between them. I created an ERD and model schema for the project based on all of the elements that I would like to include if I was able (this included the Should Have and Could Have User Story issues).

![Placeholder model schema](placeholder for model schema)

- I created an ERD for the following models:
  - User Model (Automatically created in Django framework)
  - Profile Model
  - Company Model
  - Comments Model
  - Credential Model
  - Endorse Model
  - Favourite Model

![EcoPositive Bristol User model](docs/readme-images/user-model-erd.png)
![EcoPositive Bristol Profile model](docs/readme-images/profile-model-erd.png)
![EcoPositive Bristol Company model](docs/readme-images/company-model-erd.png)
![EcoPositive Bristol Comments model](docs/readme-images/comments-model-erd.png)
![EcoPositive Bristol Credential model](docs/readme-images/credential-model-erd.png)
![EcoPositive Bristol Endorse model](docs/readme-images/endorse-model-erd.png)
![EcoPositive Bristol Favourite model](docs/readme-images/favourite-model-erd.png)

## Testing

### Automated Testing

***Companies***

- **CompanyListViewTests**
  - test_can_list_companies
  - test_logged_in_user_can_create_company
  - test_user_not_logged_in_cant_create_company

- **CompanyDetailViewTests**
  - test_can_retrieve_company_using_valid_id
  - test_cant_retrieve_company_using_invalid_id
  - test_user_can_update_own_company
  - test_user_cant_update_another_users_company