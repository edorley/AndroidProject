print "|--------------------------------------------|"
print "|         Starting Character Demo            |"
print "|--------------------------------------------|"

# Add asset paths
scene.addAssetPath('mesh', 'mesh')
scene.addAssetPath('motion', 'ChrBrad')
scene.addAssetPath("script", "behaviorsets")
scene.addAssetPath('script', 'scripts')
#added for robot
scene.addAssetPath("audio", "sounds")
scene.loadAssets()

# Set scene parameters and camera
print 'Configuring scene parameters and camera'
scene.setScale(1.0)
scene.setBoolAttribute('internalAudio', True)
scene.run('default-viewer.py')
camera = getCamera()
camera.setEye(0, 1.71, 1.86)
camera.setCenter(0, 1, 0.01)
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(1.0472)
camera.setFarPlane(100)
camera.setNearPlane(0.1)
camera.setAspectRatio(0.966897)
cameraPos = SrVec(0, 1.6, 10)
scene.getPawn('camera').setPosition(cameraPos)

# Set up joint map for Brad
print 'Setting up joint map and configuring Brad\'s skeleton'
scene.run('zebra2-map.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
bradSkeleton = scene.getSkeleton('ChrBrad.sk')
zebra2Map.applySkeleton(bradSkeleton)
zebra2Map.applyMotionRecurse('Brad')

# Establish lip syncing data set
print 'Establishing lip syncing data set'
scene.run('init-diphoneDefault.py')

# Set up face definition
print 'Setting up face definition'
# Brad's face definition
bradFace = scene.createFaceDefinition('Brad')
bradFace.setFaceNeutral('ChrBrad@face_neutral')
bradFace.setAU(1,  "left",  "ChrBrad@001_inner_brow_raiser_lf")
bradFace.setAU(1,  "right", "ChrBrad@001_inner_brow_raiser_rt")
bradFace.setAU(2,  "left",  "ChrBrad@002_outer_brow_raiser_lf")
bradFace.setAU(2,  "right", "ChrBrad@002_outer_brow_raiser_rt")
bradFace.setAU(4,  "left",  "ChrBrad@004_brow_lowerer_lf")
bradFace.setAU(4,  "right", "ChrBrad@004_brow_lowerer_rt")
bradFace.setAU(5,  "both",  "ChrBrad@005_upper_lid_raiser")
bradFace.setAU(6,  "both",  "ChrBrad@006_cheek_raiser")
bradFace.setAU(7,  "both",  "ChrBrad@007_lid_tightener")
bradFace.setAU(10, "both",  "ChrBrad@010_upper_lip_raiser")
bradFace.setAU(12, "left",  "ChrBrad@012_lip_corner_puller_lf")
bradFace.setAU(12, "right", "ChrBrad@012_lip_corner_puller_rt")
bradFace.setAU(25, "both",  "ChrBrad@025_lips_part")
bradFace.setAU(26, "both",  "ChrBrad@026_jaw_drop")
bradFace.setAU(45, "left",  "ChrBrad@045_blink_lf")
bradFace.setAU(45, "right", "ChrBrad@045_blink_rt")

bradFace.setViseme("open",    "ChrBrad@open")
bradFace.setViseme("W",       "ChrBrad@W")
bradFace.setViseme("ShCh",    "ChrBrad@ShCh")
bradFace.setViseme("PBM",     "ChrBrad@PBM")
bradFace.setViseme("FV",      "ChrBrad@FV")
bradFace.setViseme("wide",    "ChrBrad@wide")
bradFace.setViseme("tBack",   "ChrBrad@tBack")
bradFace.setViseme("tRoof",   "ChrBrad@tRoof")
bradFace.setViseme("tTeeth",  "ChrBrad@tTeeth")

print 'Adding character into scene'
# Set up Brad
brad = scene.createCharacter('Brad', '')
bradSkeleton = scene.createSkeleton('ChrBrad.sk')
brad.setSkeleton(bradSkeleton)
# Set position
bradPos = SrVec(0, 0, 0)
brad.setPosition(bradPos)
# Set facing direction
bradFacing = SrVec(0, 0, 0)
brad.setHPR(bradFacing)
# Set face definition
brad.setFaceDefinition(bradFace)
# Set standard controller
brad.createStandardControllers()
# Deformable mesh
brad.setVec3Attribute('deformableMeshScale', .01, .01, .01)
brad.setStringAttribute('deformableMesh', 'ChrBrad.dae')

# Lip syncing diphone setup
brad.setStringAttribute('lipSyncSetName', 'default')
brad.setBoolAttribute('usePhoneBigram', True)
brad.setVoice('remote')
brad.setStringAttribute("voice", "audiofile")
brad.setStringAttribute("voiceCode", ".")
'''
import platform
if platform.system() == "Windows":
	windowsVer = platform.platform()
	if windowsVer.find("Windows-7") == 0:
		brad.setVoiceCode('Microsoft|Anna')
	else:
		if windowsVer.find("Windows-8") == 0 or windowsVer.find("Windows-post2008Server") == 0:
			brad.setVoiceCode('Microsoft|David|Desktop')
else: # non-Windows platform, use Festival voices
	brad.setVoiceCode('voice_kal_diphone')'''
# note that Microsoft|Anna is the default Windows 7 voice.
#brad.setVoiceCode('Microsoft|Zira|Desktop')
# Windows 8 includes other voices: 
#Microsoft|David|Desktop

# setup locomotion
scene.run('BehaviorSetMaleMocapLocomotion.py')
setupBehaviorSet()
retargetBehaviorSet('Brad')

# setup gestures
scene.run('BehaviorSetGestures.py')
setupBehaviorSet()
retargetBehaviorSet('Brad')

# setup reach 
scene.run('BehaviorSetReaching.py')
setupBehaviorSet()
retargetBehaviorSet('Brad')
# Turn on GPU deformable geometry
brad.setStringAttribute("displayType", "GPUmesh")

# Set up steering
print 'Setting up steering'
steerManager = scene.getSteerManager()
steerManager.setEnable(False)
brad.setBoolAttribute('steering.pathFollowingMode', False) # disable path following mode so that obstacles will be respected
steerManager.setEnable(True)
# Start the simulation
print 'Starting the simulation'
sim.start()

bml.execBML('Brad', '<body posture="ChrMarine@Idle01"/>')
bml.execBML('Brad', '<saccade mode="listen"/>')
#bml.execBML('ChrBrad', '<gaze sbm:handle="brad" target="camera"/>')

sim.resume()
