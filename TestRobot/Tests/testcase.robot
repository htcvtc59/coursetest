*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library
Documentation               Present some information about this test suite
Library                     Selenium2Library
*** Variables ***

*** Test Cases ***
Valid Login
    [Documentation]                     Present some information about this test case

    open browser                        http://localhost:8000   chrome
    wait until page contains            Vui lòng đăng nhập!
    input text                          id=__BVID__1         admincourse
    input password                      id=__BVID__2         admincourse
    Click Button                          xpath=//button[@type='submit']
    wait until page contains            Đăng xuất
    CLick Link                          Đăng xuất
    close browser

Create Account
    open browser                        http://localhost:8000   chrome
    wait until page contains            Vui lòng đăng nhập!
    input text                          id=__BVID__1         admincourse
    input password                      id=__BVID__2         admincourse
    Click Button                          xpath=//button[@type='submit']
    wait until page contains            Đăng xuất

    Go To                                 http://localhost:8000/app/users/
    wait until page contains            Học viên
    Click Button                         xpath=(//button[@type='button'])[3]
    input text                                  id=exstudent1   hv1
    Choose File                              id=exstudent2    /Users/oh/Downloads/identicon.png
    input text                                 id=exstudent3   Nguyễn Văn A
    input text                                  id=exstudent4    hs1@gmail.com
    input text                                  id=exstudent5    1234
    Click Element                                 id=addnewstudent
    Wait Until Element Is Not Visible                      id=addnewstudent
    Click Link                                   id=__BVID__28___BV_tab_button__
    Click Button                                 xpath=(//button[@type='button'])[9]
    input text                                      id=exampleInput1  gv1
    Choose File                                   id=exampleInput2  /Users/oh/Downloads/identicon.png
    input text                                   id=exampleInput3    Nguyễn Văn B
    input text                                   id=exampleInput4    gv1@gmail.com
    input text                                   id=exampleInput5    1234
    Click Element                                      id=addnewteacher
    Wait Until Element Is Not Visible                      id=addnewteacher
    Click Element                                //table[@id='dataTableTeacher']/tbody/tr/td[2]
    Click Button                                         id=vdeleteteacherbtn
    Wait Until Element Is Not Visible                      id=vdeleteteacherbtn
     Go To                                 http://localhost:8000/app/users/
    Click Element                                        //table[@id='dataTableStudent']/tbody/tr/td[3]
    Click Button                                          id=vdeletestudentbtn
    Wait Until Element Is Not Visible                      id=vdeletestudentbtn
    Go To                                 http://localhost:8000/app/users/
    wait until page contains            Đăng xuất
    CLick Link                          Đăng xuất
    close browser