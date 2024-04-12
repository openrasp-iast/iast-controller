# IAST-CONTROLLER

IAST-CONTROLLER is a tool for managing IAST (Intelligent Application Security Testing) test cases. It is a web application that allows you to manage test cases, test suites, and test environments. It also allows you to manage test results and generate reports.

## Installation

### Requirements

- Python 3.6+
- MySQL 5.7+
- Redis 3.0+

### Installation

```bash
# Clone the repository
git clone https://github.com/IAST-Project/IAST-CONTROLLER.git

# Install dependencies
pip install -r requirements.txt

# Create a MySQL database and update the configuration
vi config.py

# Run the application
python manage.py runserver
```

## Usage

### Creating a Test Case

```bash
# Migrate the database
python manage.py migrate

# create admin user
python manage.py createsuperuser
```

### TODO

```bash
相比于开源版本，商业版具有如下高级功能:
动态污点追踪。能够识别关键参数的来源，预判接口是否存在漏洞。
漏洞检测能力更强。支持NoSQL注入等22类攻击检测，硬编码密码等30类基线检测。
多账号体系和权限管理。可创建多个用户，并授予不同的权限。
自动升级支持。自动识别应用目录并部署，后续版本随应用重启而升级，无需再次部署。
第三方类库弱点识别。开源版本仅采集类库信息，商业版同时判断是否存在已知漏洞。
可视化图表支持。支持漏洞报告导出，以及更加全面的报表展示。
目前，商业版核心功能已经开发完毕，预计3~4月份可申请试用，具体时间请留意QQ群公告。
```

### Creating a Test Case

1. Go to the "Test Cases" page.
2. Click the "Create Test Case" button.
3. Enter the test case name and description.
4. Click the "Create" button.

### Creating a Test Suite

1. Go to the "Test Suites" page.
2. Click the "Create Test Suite" button.
3. Enter the test suite name and description.
4. Click the "Create" button.

### Creating a Test Environment

1. Go to the "Test Environments" page.
2. Click the "Create Test Environment" button.
3. Enter the test environment name and description.
4. Click the "Create" button.

### Creating a Test Result

1. Go to the "Test Results" page.
2. Click the "Create Test Result" button.
3. Enter the test result name and description.
4. Click the "Create" button.

### Generating a Report

1. Go to the "Reports" page.
2. Click the "Generate Report" button.
3. Select the test suite and test environment.
4. Click the "Generate" button.

## License

IAST-CONTROLLER is released under the [Apache 2.0 license](LICENSE).

## Contact

If you have any questions, please contact us via email:

**Email:** g3g4x5x6@foxmail.com

## Libs

- https://github.com/antlr/antlr4
- https://github.com/andialbrecht/sqlparse
- https://github.com/idank/bashlex
