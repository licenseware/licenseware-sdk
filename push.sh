#!/bin/bash

GIT='git --git-dir='$PWD'/.git'

$GIT init
$GIT checkout -b main
$GIT add .
$GIT commit -m "push boilerplate to main"
$GIT remote add origin git@github.com:licenseware/lware-components.git
$GIT push origin --force main


