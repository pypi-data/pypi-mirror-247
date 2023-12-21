# FOSSLIGHT CLI

FOSSLIGHT Hub 서버에 간편하게 요청을 보낼 수 있는 도구입니다.<br>
프로젝트 생성, 수정, 분석, 분석파일 업로드, bom export 등 다양하게 활용할 수 있습니다.

# 📋 Prerequisite
Python 3.8+

# 🎉 How to install
```
$ pip3 install fosslight_cli
```

# How to Run

터미널 창에서 fosslight-cli 명령을 실행하려면 다음의 구문을 사용한다.

```
$ fosslight-cli [command] [resource name] ([sub-resource name]) [parameters ...]
```

- **command**: 수행하려는 동작을 지정한다.
    - create
    - update
    - get
    - export
    - apply
    - compare
- **resource name**: 리소스 이름을 지정한다.
    - project
    - selfCheck
    - config
    - code
    - partner
    - oss
    - license
    - vulnerability
    - maxVulnerability
    - yaml
- **sub-resource name**: 일부 명령은 하위 리소스 이름을 지정해주어야 한다.
    - ex.
        
        ```
        $ fosslight-cli get project list
        $ fosslight-cli update project bin
        $ fosslight-cli get project models
        ```
- **parameters**: 입력 파라미터 목록. 필수 파라미터와 선택 파라미터를 입력할 수 있다.


# 명령어
| 명령어 | 구문                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 설명 |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| --- |
| create |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 리소스 생성 |
|  | fosslight-cli create project <br>&nbsp; --prjName TEXT            Name of the Project  [required] <br>&nbsp; --osType TEXT             OS type of the Project  [required] <br>&nbsp; --distributionType TEXT   [required] <br>&nbsp; --networkServerType TEXT  [required] <br>&nbsp; --priority TEXT           [required] <br>&nbsp; --osTypeEtc TEXT <br>&nbsp; --prjVersion TEXT <br>&nbsp; --publicYn TEXT <br>&nbsp; --comment TEXT <br>&nbsp; --userComment TEXT <br>&nbsp; --watcherEmailList TEXT <br>&nbsp; --modelListToUpdate TEXT <br>&nbsp; --modelReportFile TEXT | 프로젝트 생성 |
|  | fosslight-cli create selfCheck <br>&nbsp; --prjName TEXT     Name of the Project  [required] <br>&nbsp; --prjVersion TEXT  Version of the Project                                                                                                                                                                                                                                                                                                                                                                  | self-check 생성 |
| update |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 리소스 수정 |
|  | fosslight-cli update project watchers <br>&nbsp; --prjId TEXT      project id  [required] <br>&nbsp; --emailList TEXT  watcher emailList  [required]                                                                                                                                                                                                                                                                                                                                                               | 프로젝트 watcher 변경 |
|  | fosslight-cli update project models <br>&nbsp; --prjId TEXT              project id  [required] <br>&nbsp; --modelListToUpdate TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                    | 프로젝트 모델 목록 수정 |
|  | fosslight-cli update project modelFile <br>&nbsp; --prjId TEXT        project id  [required] <br>&nbsp; --modelReport TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                             | 모델 파일을 이용하여 프로젝트 모델 목록 수정 |
|  | fosslight-cli update project scan <br>&nbsp; --prjId TEXT  project id  [required] <br>&nbsp; --dir TEXT    project directory path  [required]                                                                                                                                                                                                                                                                                                                                                                      | 프로젝트 디렉토리를 fosslight scanner를 이용하여 분석한 후 bin, src 파일 업로드 |
|  | fosslight-cli update project bin <br>&nbsp; --prjId TEXT      project id  [required] <br>&nbsp; --ossReport TEXT <br>&nbsp; --binaryTxt TEXT <br>&nbsp; --comment TEXT <br>&nbsp; --resetFlag TEXT                                                                                                                                                                                                                                                                                                                                   | 프로젝트 bin 파일 업로드  |
|  | fosslight-cli update project src <br>&nbsp; --prjId TEXT      project id  [required] <br>&nbsp; --ossReport TEXT <br>&nbsp; --comment TEXT <br>&nbsp; --resetFlag TEXT                                                                                                                                                                                                                                                                                                                                                         | 프로젝트 src 파일 업로드  |
|  | fosslight-cli update project package <br>&nbsp; --prjId TEXT        project id  [required] <br>&nbsp; --packageFile TEXT  [required] <br>&nbsp; --verifyFlag TEXT                                                                                                                                                                                                                                                                                                                                                        | 프로젝트 package 파일 업로드 |
|  | fosslight-cli update selfCheck report <br>&nbsp; --selfCheckId TEXT  selfCheck id  [required] <br>&nbsp; --ossReport TEXT <br>&nbsp; --resetFlag TEXT                                                                                                                                                                                                                                                                                                                                                                    | self-check report 파일 업로드 |
|  | fosslight-cli update selfCheck watchers <br>&nbsp; --selfCheckId TEXT  selfCheck id  [required] <br>&nbsp; --emailList TEXT    [required]                                                                                                                                                                                                                                                                                                                                                                          | self-check watcher 변경 |
|  | fosslight-cli update partner watchers <br>&nbsp; --partnerId TEXT  partner id  [required] <br>&nbsp; --emailList TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                                  | partner watcher 변경 |
|  | fosslight-cli update config <br>&nbsp; -s, --server TEXT  Server url <br>&nbsp; -t, --token TEXT   Account token                                                                                                                                                                                                                                                                                                                                                                                                   | 서버, 인증토큰 설정 |
| get |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 리소스를 가져옴 |
|  | fosslight-cli get project list <br>&nbsp; --createDate TEXT <br>&nbsp; --creator TEXT <br>&nbsp; --division TEXT <br>&nbsp; --modelName TEXT <br>&nbsp; --prjIdList TEXT <br>&nbsp; --status TEXT <br>&nbsp; --updateDate TEXT                                                                                                                                                                                                                                                                                                                   | 프로젝트 목록 출력 |
|  | fosslight-cli get project models <br>&nbsp; --prjIdList TEXT                                                                                                                                                                                                                                                                                                                                                                                                                 | 프로젝트 모델목록 출력 |
|  | fosslight-cli get license list <br>&nbsp; --licenseName TEXT  license name  [required]                                                                                                                                                                                                                                                                                                                                                                                                                       | 라이센스 목록 출력 |
|  | fosslight-cli get oss list <br>&nbsp; --ossName TEXT           oss name  [required] <br>&nbsp; --ossVersion TEXT        oss version <br>&nbsp; --downloadLocation TEXT  download location                                                                                                                                                                                                                                                                                                                                | oss 목록 출력 |
|  | fosslight-cli get partner list <br>&nbsp; --createDate TEXT <br>&nbsp; --creator TEXT <br>&nbsp; --division TEXT <br>&nbsp; --partnerIdList TEXT <br>&nbsp; --status TEXT <br>&nbsp; --updateDate TEXT                                                                                                                                                                                                                                                                                                                                     | 3rd party 목록 출력 |
|  | fosslight-cli get config                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 설정된 서버, 인증토큰 출력 |
|  | fosslight-cli get code <br>&nbsp; --codeType TEXT     code type  [required] <br>&nbsp; --detailValue TEXT  detail value                                                                                                                                                                                                                                                                                                                                                                                            | 코드 정보 출력 |
|  | fosslight-cli get maxVulnerability <br>&nbsp; --ossName TEXT     oss name  [required] <br>&nbsp; --ossVersion TEXT  oss version                                                                                                                                                                                                                                                                                                                                                                                    | max vulnerability 출력 |
|  | fosslight-cli get vulnerability <br>&nbsp; --cveId TEXT       cve id <br>&nbsp; --ossName TEXT     oss name <br>&nbsp; --ossVersion TEXT  oss version                                                                                                                                                                                                                                                                                                                                                                    | vulnerability 정보 출력 |
| export |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 리소스(주로 파일)을 가져옴 |
|  | fosslight-cli export project bom <br>&nbsp; --prjId TEXT          project id  [required] <br>&nbsp; --mergeSaveFlag TEXT  mergeSaveFlag <br>&nbsp; -o, --output TEXT     output file path                                                                                                                                                                                                                                                                                                                                | 프로젝트 bom 파일 다운로드                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|  | fosslight-cli export project bomJson <br>&nbsp; --prjId TEXT  project id  [required]                                                                                                                                                                                                                                                                                                                                                                                                                         | 프로젝트 bom 정보를 json으로 출력 |
|  | fosslight-cli export project notice <br>&nbsp; --prjId TEXT       project id  [required] <br>&nbsp; -o, --output TEXT  output file path                                                                                                                                                                                                                                                                                                                                                                            | 프로젝트 고지문 파일 다운로드                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|  | fosslight-cli export selfCheck <br>&nbsp; --selfCheckId TEXT  selfCheck id  [required]                                                                                                                                                                                                                                                                                                                                                                                                                       | self-check export |
| compare |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 리소스 비교 |
|  | fosslight-cli compare project bom <br>&nbsp; --prjId TEXT      [required] <br>&nbsp; --compareId TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                                                  | 두 프로젝트의 bom을 비교                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| apply |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 파일에 정의된 동작을 수행 |
|  | fosslight-cli apply yaml <br>&nbsp; -f, --file TEXT  yaml file path  [required]                                                                                                                                                                                                                                                                                                                                                                                                                              | yaml 파일을 입력으로 받아서 적절한 동작을 수행.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

# Apply

파일에 정의된 동작을 한번에 수행하는 기능.

kind 값에 따라 동작을 구분한다.

### createProject

ex. 

- fosslight-cli apply yaml -f create_project.yaml
    
    ```yaml
    # create_project.yaml
    kind: createProject
    parameters:
      prjName: test-project
      prjVersion: 1
      osType: Linux
      distributionType: "General Model"
      networkServerType: N
      priority: P1
    update:
      models:
        modelListToUpdate: "ASDF|AV/Car/Security > AV|20201010"
    scan:
      dir: "~/data/simpleProject"
    ```
    
    - 프로젝트를 생성하고, model 정보를 업데이트한 뒤 프로젝트 디렉토리를 scan한 결과를 업로드한다.
