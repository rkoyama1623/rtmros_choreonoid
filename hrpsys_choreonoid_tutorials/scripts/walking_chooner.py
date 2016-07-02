import jaxon_red_setup
import sys
import numpy as np
import time

class walking_chooner(jaxon_red_setup.JAXON_RED_HrpsysConfigurator):
    def __init__(self,*args, **kwargs):
        jaxon_red_setup.JAXON_RED_HrpsysConfigurator.__init__(self,*args, **kwargs)
        self.refVel=np.zeros(3)
        self.actVel=np.zeros(3)
        self.goalVel=np.zeros(3)

        #constants
        self.maxAcc=np.array([0.5,0.5,10])
        self.maxTimeDiffRatio=0.7

    def getParams(self):
        self.pg=self.abc_svc.getGaitGeneratorParam()[1]
        self.pa=self.abc_svc.getAutoBalancerParam()[1]
    def goVelocity(self,vx,vy,vt):
        vel=np.array([vx,vy,vt])
        self.refVel=vel
        self._goVelocity(vel)
    def _goVelocity(self,vel):
        self.refVel=vel
        self.abc_svc.goVelocity(vel[0],vel[1],vel[2])
    def getCurrentRefVelocity(self):
        self.refVel
    def getCurrentActVelocity(self):#todo
        self.getParams()
        fsl=self.abc_svc.getRemainingFootstepSequence()[1]
        tm=self.pg.default_step_time
        vel1= np.linalg.norm(np.array(fsl[1].pos)-np.array(fsl[0].pos))/tm
        vel2= np.linalg.norm(np.array(fsl[2].pos)-np.array(fsl[0].pos))/(2*tm)
        print vel2
        print fsl[0].pos
        print fsl[1].pos
        print fsl[2].pos
    def setGoalVel(self,vx,vy,vt):
        self.goalVel=np.array([vx,vy,vt])
        self.getParams()
        tm=self.pg.default_step_time
        maxAccOneTick=self.maxAcc*tm
        stepsToAccel=np.max(np.ceil(np.abs(self.goalVel-self.refVel)/maxAccOneTick))
        if int(stepsToAccel)==0:
            stepsToAccel=1
        AccOneTick=(self.goalVel-self.refVel)/float(stepsToAccel)
        print AccOneTick
        for i in range(int(stepsToAccel)):
            self.refVel=self.refVel+AccOneTick
            self._goVelocity(self.refVel)
            print "goVelocity",
            print self.refVel
            time.sleep(tm*3)
        self.refVel=self.goalVel
        self._goVelocity(self.refVel)
        print "goVelocity",
        print self.refVel
        time.sleep(tm)


    def setGoalDefaultStepTime(self,tt):
        self.getParams()
        tm=self.pg.default_step_time

        steps=np.ceil(np.log(tt/tm)/np.log(self.maxTimeDiffRatio))

        for i in range(int(steps)-1):
            tm=self.pg.default_step_time
            ratio=self.pg.default_double_support_ratio
            tm2=self.pg.default_step_time*self.maxTimeDiffRatio
            ratio2=self.pg.default_double_support_ratio*self.maxTimeDiffRatio
            print "set default_step_time/ratio:",tm2,ratio2
            self.pg.default_step_time=tm2
            self.pg.default_double_support_ratio=ratio2
            self.abc_svc.setGaitGeneratorParam(self.pg)
            time.sleep(tm*2)
        ratio2=self.pg.default_double_support_ratio*(tt/self.pg.default_step_time)
        self.pg.default_step_time=tt
        print "set default_step_time/ratio:",tt,ratio2
        self.abc_svc.setGaitGeneratorParam(self.pg)


if __name__ == '__main__':
    hcf = walking_chooner("JAXON_RED")
    [sys.argv, connect_constraint_force_logger_ports] = hcf.parse_arg_for_connect_ports(sys.argv)
    hcf.init("JAXON_RED(Robot)0", connect_constraint_force_logger_ports=connect_constraint_force_logger_ports)
    hcf.startABSTIMP()

# p=hcf.abc_svc.getGaitGeneratorParam()[1]
# pa=hcf.abc_svc.getAutoBalancerParam()[1]
