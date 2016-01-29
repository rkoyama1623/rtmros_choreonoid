#!/bin/sh

# PROJECT_FILE:=
dir=$HOME/barbell
rtmtest -t hrpsys_tools _gen_project.launch \
INPUT:=`rospack find hrp2_models`/HRP2JSKNT_for_OpenHRP3/HRP2JSKNTmain.wrl \
OUTPUT:=`pwd`/$1.xml \
OBJECT_MODELS:=\
"`zenity --file-selection --filename="$dir/trass_main.wrl" --file-filter=*.wrl`,1,0,0,0,0,0,0, \
`rospack find openhrp3`/share/OpenHRP-3.1/sample/model/longfloor.wrl,0,0,0,1,0,0,0" \
CORBA_PORT:=15005 INTEGRATE:=true CONF_DT_OPTION:="--dt 0.002" SIMULATION_TIMESTEP_OPTION:="--timeStep 0.002"
#SIMULATION_JOINT_PROPERTIES_OPTION:="--use-highgain-mode false" ## for ST


#INPUT:=`rospack find jsk_models`/JAXON_RED/JAXON_REDmain.wrl \