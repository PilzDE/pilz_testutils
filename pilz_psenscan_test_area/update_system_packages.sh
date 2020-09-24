#!/bin/bash -x

update_system_packages()
{
  sudo apt-get update -qq && sudo apt-get upgrade -qq
}

update_system_packages
