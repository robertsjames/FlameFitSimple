#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tina Pollmann
@year: 2022

"""

import math
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import colors as colors
import matplotlib.patches as patches


#constants
SecondsPerYear = 365.*24.*60.*60.
LXeDensity = 2.869 #g/cm^3 at 1.8bar

#LXeDensity = 2.9 

''' 
Light and charge yields from NEST. If this file is missing, use FetchNESTData.ipynb to
generate it. It takes data from https://nest.physics.ucdavis.edu/benchmark-plots
'''
f_NEST = open("/Users/amirr/Desktop/Flame/FlameFitSimple/analyses/wimp_sensitivity/AC_background/nestyields_XLZD.txt")
data = json.load(f_NEST)

'''
This retrieves the number of electrons or photons that will be produced on average for a given energy deposit.
particle: can be "ER" in which case the curve for a beta is looked up, or "NR" (curve for neutrons) 

energy: in keV, the energy deposit
signal: can be "photons" or "electrons", select which one you want to know the number of quanta for
field: the drift field strength in V/cm; only a few options for the field will be available, depending on what was downloaded 
	with FetchNESTData.ipynb

Returns one number, the total number of quanta produced of the desired type
'''
def ReadNest(particle, energy, signal, field):
	particle_name = ""
	binning = 0.25
	energies = []
	if particle=="ER":
		particle_name = "beta"
		energies = data["energiesER"]
	elif particle=="NR":
		binning = 0.5
		energies = data["energiesNR"]
		particle_name ="neutron"
	else:
		print("Error, particle type not supported")
		

	if field not in data["fields"]:
		print("Field not supported")
		return 0.0
	#Find the array position for this energy
	pos = -1

	for i in list(range(len(energies))):
		if abs(energy - energies[i]) < binning:
			pos = i
			continue 											
	if pos < 0:
		print("Error, energy " + str(energy) + " not found.")
		return 0.0
	value = data[particle_name][str(field)][signal][pos] 		
	if value < 0.:												
		value = 0.0 #happens when NEST lookup is out of range at very low energies
	return data[particle_name][str(field)][signal][pos]	

		
#functions
def Poisson(l,k):
	return np.power(l, k) * np.exp(-l) / np.math.factorial(int(np.rint(k)))
PoissonV = np.vectorize(Poisson)
def Gaus(x, mu, sig):
		return 1./(np.sqrt(2*np.pi)*sig) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


## Utility
def GaussianFilter(R,S1,S2,binwidth,maxS1Range, maxS2Range, ENF):
	S1c, S2c = np.meshgrid(np.linspace(1,maxS1Range,maxS1Range), np.linspace(1,maxS2Range,maxS2Range))
	R_z = S1c
	iskipped = []
	gmatrix = S1c
	print("It may take a moment for the blurring to finish.")
	for i in range(len(R)):

		sig1 = 1.4
		sig2 = 1.4
		if S1[i] > 0:
			sig1 = (1.+ENF)*np.sqrt(S1[i])
		if S2[i] > 0:
			sig2 = (1.+ENF)*np.sqrt(S2[i])
		'''There isnt a great way to blur at the edges while retaining the amplitude.
		This condition will introduce an effect at the upper edge.'''
		if S1[i] > maxS1Range-3*sig1 or S2[i] > maxS2Range-3*sig2:
			iskipped.append(i)
			continue			
		gmatrix = np.exp(-(((S1c-S1[i])**2/(2.0 * sig1**2) + (S2c-S2[i])**2/(2.0 * sig2**2)))) # This is really slow; could be improved if manually looping on the 2D space and skipping bins more than 3 sigma away from the centers
		amplitude = sum(map(sum, gmatrix))
		''' Just normalizing the gaussian in the calculation above doesnt work.
			First divide by ammplitude to make the integral 1.
			Then multiply by R[i] to get the total rate desired.
			The rates are "per keV" but to get a continuous distribution here, we split
			each keV into smaller steps of a certain binwidth. To get back to a rate 
			"per keV", multiply by this binwidth.
		'''
		gmatrix = gmatrix*R[i]*binwidth/amplitude
		if (i == 0):
			R_z = gmatrix
		else:
			R_z = R_z + gmatrix
	
	''' Sanity check of the total rate across this 2D space. Make sure that the total rate input
		is the same as the rate that comes out. '''
	gsum=0
	osum=0
	for k in range(len(R_z)):
		for l in range(len(R_z[0])):
			gsum = gsum + R_z[k,l]
	for i in range(len(R)):
		if i in iskipped:
			continue
		osum = osum + R[i]*binwidth
	if (abs(gsum - osum)/gsum > 0.01):
		#This is a consistency check to make sure we are conserving the rates
		print("Error: gaussian blur not successful. Rates will not be correct.")
	return S1c, S2c, R_z


def GaussianFilterGPT(R, S1, S2, binwidth, maxS1Range, maxS2Range, ENF, g2):

	
    S1c, S2c = np.meshgrid(np.arange(1, maxS1Range + 1, maxS1Range/250), np.logspace(2, 4.75, 110+1)/g2, indexing='ij') # Use 'ij' indexing 
    R_z = np.zeros_like(S1c, dtype=float)  # Specify the data type explicitly
    iskipped = []

    print("It may take a moment for the blurring to finish.")
    
    for i in range(len(R)):
        sig1 = 1.4
        sig2 = 1.4

        if S1[i] > 0:
            sig1 = (1.0 + ENF) * np.sqrt(S1[i])
        if S2[i] > 0:
            sig2 = (1.0 + ENF) * np.sqrt(S2[i])

        # Calculate Gaussian values efficiently without explicit loops
        diff1 = S1c - S1[i]
        diff2 = S2c - S2[i]
        gmatrix = np.exp(-((diff1**2) / (2.0 * sig1**2) + (diff2**2) / (2.0 * sig2**2)))

        # Normalize the Gaussian matrix
        amplitude = np.sum(gmatrix)
        if amplitude > 0:
            gmatrix *= R[i] * binwidth / amplitude
        else:
            iskipped.append(i)

        # Add the Gaussian matrix to the result
        R_z += gmatrix
    
    # Sanity check of the total rate across this 2D space
    gsum = np.sum(R_z)
    osum = np.sum(R) * binwidth

    if abs(gsum - osum) / gsum > 0.01:
        print("Error: gaussian blur not successful. Rates will not be correct.")

    return S1c, S2c, R_z
    	
def GaussianFilter1D(R,S1,binwidth,maxS1Range, ENF):
	R_smeared = []
	S1c = np.linspace(1,len(R),len(R))
	for i in range(len(R)):
		sig1 = 1
		if S1[i] > 0:
			sig1 = (1.+ENF)*np.sqrt(S1[i])
		'''There isnt a great way to blur at the edges while retaining the amplitude.
		This condition will introduce an effect at the upper edge.'''
		if S1[i] > maxS1Range-3*sig1:
			continue			
		R_new = R[i] * Gaus(S1c, S1[i], sig1)
		if (i == 0):
			R_smeared = R_new
		else:
			R_smeared = R_smeared + R_new	
	R1 = 0
	R2 = 0
	for i in range(len(R)):
		R1 = R1 + R[i]	
		R2 = R2 + R_smeared[i]
	print(str(R1) + ", " + str(R2))
	return R_smeared

def GaussianFilter1DGPT(R, S1, binwidth, maxS1Range, ENF):
    S1c = np.arange(1, len(R) + 1)
    sig1 = np.where(S1 > 0, (1.0 + ENF) * np.sqrt(S1), 1.0)

    # Create a Gaussian kernel for all S1 values
    kernel = np.exp(-((S1c - 1 - S1) ** 2) / (2.0 * sig1**2))

    # Apply the Gaussian kernel to R using vectorized operations
    R_smeared = np.sum(R[:, np.newaxis] * kernel, axis=1)

    # Calculate the total sums using NumPy's sum function
    R1 = np.sum(R)
    R2 = np.sum(R_smeared)
    print(f"{R1}, {R2}")

    return R_smeared


''' 
Convert the drift field strength to the electron drift speed.
The relation between the two is based on a fit to Fig. 5 in http://arxiv.org/abs/1609.04467, 
and valid for fields between approximately 50 and 200 V/cm.
DriftField: field strength in V/cm

Return: the electron drift speed in mm/us
'''
def fElectronDriftSpeed(DriftField):
	a = 0.2459
	b =	 -0.30527
	return a/np.power(DriftField,b) #mm/us = 100 cm/ms = 1000 m/s

def fToMass(radius, height): 
	'''Radius and height should be in cm. Result will be in tonnes.'''
	return np.pi * np.power(radius, 2) * height *  LXeDensity * 1e-6 


''' 
The S1 coincidence window length is determined by the Xe2* singlet decay time and by scattering
in the detector. Scattering very roughly goes with detector size. In the absence of better data,
we take two known detectors and their coincidence windows:
50 ns for 1T size and 200 ns for DARWIN size
and let's extrapolate linearly between those two, with height for now (FIXME).
This will return nonsense for detectors smaller than XENON1T because the minimum window length
to accommodate the finite decay time is not considered separately.

height: detector height in cm

Returns the estimated length of the S1 coincidence window in ns.
'''
def fS1CoincidenceWindow(height): #time window - within this time (ns) we count smth as a possible S1. decay time of xenon triplet - 30 ns. so 60 ns will already give you all S1. 
	return -50. + 1.*height


'''
This class stores all the detector geometry and performance parameters relevant to ACs.
Required parameters that are not explicitly input during construction are calculated below. 
Since this model is to work for detectors of different sizes, we try to estimate how parameters
such as S1CoincidenceWindow depend on the detector height and then calculate them here
rather than asking the user to input them.

BelowCathodeHeight: This is the height of the charge insensitive volume below the cathode
FiducialCut: A cut in R that defines the fiducial volume. The fiducial volume is a cylinder 
with radius (TPCRadius-FiducialCut) and height TPCHeight. This misses the fiducial cut in
z, or any non-cylindrical geometries, but is probably good enough.

ExtractionEfficiency: For electrons at the liquid/gas boundary. Currently not used.

LCETop/LCEBottom: light collection efficiency at the top and bottom of the TPC. The LCE as a 
function of z will be linearly interpolated between the two. 

PMTDetectionProb: This is largely the quantum efficiency of the PMTs. It is used together with 
LCETop and LCEBottom to calculate g1.

PMTDensity: This is the average number of photo sensors per area. This is used to scale to
the approximate number of sensors needed for a given radius. 

'''
class Detector:
	def __init__(self,
			   TPCHeight,	# cm
			   TPCRadius,	# cm
			   BelowCathodeHeight, # cm
			   FiducialCut, # cm
			   ExtractionEfficiency, # fraction
			   g2,	 # PE/(extracted electron)
			   g1, 
			   SEGain, #single electron gain
			   LCETop,	# fraction
			   LCEBottom,  # fraction
			   PMTDetectionProb, # fraction
			   PMTDarkRate,	 # Hz
			   DriftField,	 # V/cm
			   ElectronLifetime,  # ms
			   PMTDensity,	#PMTs/cm^2
			  ):
		
		self.height = TPCHeight
		self.radius = TPCRadius
		self.BelowCathodeHeight = BelowCathodeHeight   # The charge-insensitive volume
		self.FiducialCut = FiducialCut				   # The fiducial volume is a perfect cylinder 'FiducialCut' away from the TPC
		self.ExtractionEfficiency = ExtractionEfficiency # For S2 electrons
		self.g2 = g2
		self.g1 = g1 
		self.SEGain = SEGain
		self.LCETop = LCETop	  #Light collection efficiency, without PMT quantum efficiency multiplied in
		self.LCEBottom = LCEBottom
		self.PMTDetectionProb = PMTDetectionProb
		self.PMTDarkRate = PMTDarkRate	# Hz
		self.DriftField = DriftField	# V/cm
		self.ElectronLifetime = ElectronLifetime # ms

		self.ElectronDriftSpeed = fElectronDriftSpeed(DriftField)*100. #cm/ms
		self.MaxDriftTime = TPCHeight/self.ElectronDriftSpeed*1e6      # ns 
		self.activeMass = fToMass(TPCRadius,TPCHeight)
		self.TPCArea = TPCHeight * 2*np.pi*TPCRadius + np.pi*TPCRadius*TPCRadius 
		self.TPCLidArea = np.pi*TPCRadius*TPCRadius
		self.fiducialMass = fToMass(self.radius-FiducialCut, TPCHeight)	 #tonne; we dont' subtract the fiducial cut from z, because this is used later to calculate the lone rates, where we can no longer make a cut in z
		self.S2BlindMass = fToMass(self.radius, BelowCathodeHeight)      # in the charge-insensitive region below the cathode

		#self.g1 = PMTDetectionProb*(LCETop + LCEBottom)/2. 
		
		self.S1CoincidenceWindow = fS1CoincidenceWindow(TPCHeight)
 
		self.PMTs = int(self.radius**2. * np.pi * PMTDensity)  # We assume same PMT density per area as in 1T, so just scale the number by the relative areas
		
		self.TotalDNRate = self.PMTDarkRate*self.PMTs
		
	''' Yields the number of photons and electrons produced for a given energy and interaction type,
		based on NEST tables and including the proper rate of each type of background. '''
	def EnergyToQuanta(self, energy, interaction):
		S1 = ReadNest(interaction,energy,"photons",self.DriftField)
		S2 = ReadNest(interaction,energy,"electrons",self.DriftField)
		return S1, S2
				
	def __str__(self):
		return "the fiducial mass is " + "{:.2f}".format(self.fiducialMass) + " tonnes" + "\n" + \
		"		the active mass is " + "{:.2f}".format(self.activeMass) + " tonnes"+ "\n" + \
		"		the below-cathode mass is " + "{:.2f}".format(self.S2BlindMass) + " tonnes"+ "\n" + \
		"		the drift speed is " + "{:.2f}".format(self.ElectronDriftSpeed) + "cm/ms"+ "\n" + \
		"		the max drift time is " + "{:.2f}".format(self.MaxDriftTime * 1e-6) + "ms"+ "\n" + \
		"		the number of PMTs is " + str(self.PMTs) + " "+ "\n" + \
		"		g1 is " + "{:.2f}".format(self.g1)

		
	

'''
This class stores information related to particle-induced backgrounds. All the rates input are 
per area or per volume, and will be scaled up to the area or volume of the detector given as input.
There are also utility functions that assemble the ER and NR spectra needed later in the 
model for the lone S1 and lone S2 spectra.

NR:
CEvNS - modelled as a double exponential spectrum 
Neutrons - modelled as a single exponential spectrum

ER:
Total ER rate in the relevant energy window where ~ < 200 photons are produced is approximately flat,
so we model it as flat. Individual contributions are not considered separately, only the sum spectrum.

For neutrons and ER, both the rate inside and outside the fiducial volume have to be specified.
The fiducial volume - or more precisely the FV cut in radius, has to be provided correctly to
the 'detector' class.
'''
class ParticleBackground:
	def __init__(self,
				 detector,
				 A1_cevns,	# events per (tonne year)
				 b1_cevns,	# keV
				 A2_cevns,	# events per (tonne year)
				 b2_cevns,	# keV
				 A_neutrons_fiducial,  # events per (cm^2 year)
				 A_neutrons_edge,	   # events per (cm^2 year)
				 b_neutrons, # keV
				 FlatERRate_internal,  # Rn, Kr - events per (kev tonne year) 
				 FlatErRate_external,  # Materials - events per (kev cm^2 year)
				):
		self.detector = detector
		if detector is None:
			print("Class:ParticleBackground Error: Detector must not be None.") #Fixme, throw a proper error
		self.A1_cevns = A1_cevns
		self.b1_cevns = b1_cevns
		self.A2_cevns = A2_cevns
		self.b2_cevns = b2_cevns
		self.A_neutrons_fiducial = A_neutrons_fiducial #not used below
		self.A_neutrons_edge = A_neutrons_edge
		self.b_neutrons = b_neutrons
		self.FlatERRate_internal = FlatERRate_internal
		self.FlatErRate_external = FlatErRate_external
		
	''' Define the spectra, given shapes and rates. Returns events/year/keV'''
	def BackgroundSpectrum(self, energy, interaction, location, mass=-1, area=-1):
		rate = -1
		if interaction=="ER" and location=="internal":
			rate = self.FlatERRate_internal*mass *energy/energy #flat bg rate 
		elif interaction=="ER" and location=="external" :
			rate =	self.FlatErRate_external*area*energy/energy # fixme - give me a better shape
		elif interaction=="NR" and location=="internal":
			rate = self.A1_cevns/self.b1_cevns*mass*np.exp(-energy/self.b1_cevns) + self.A2_cevns/self.b2_cevns*mass*np.exp(-energy/self.b2_cevns)	
			# the rate scales with mass (solar neutrinos)
		elif interaction=="NR" and location=="external":
			rate = self.A_neutrons_edge/self.b_neutrons * area *np.exp(-energy/self.b_neutrons)
		return rate
	
	'''
	Lone S1 and Lone S2 are created in different regions of the detector. Explanations are 
	inside the function.
	
	energy: in keV
	signal: "S1" or "S2"
	interaction: "ER" or "NR"
	'''
	def BackgroundSpectraForLone(self, energy, signal, interaction):
		rate = -1
		# Backgrounds relevant to lone-s1
		# The internal rate of ER and NR in (active mass) + external rate on TPC area (including bottom,lid). Note that charge inesnsitive volume will be treated independently, since it only makes an S1 
		if interaction=="ER" and signal=="S1":
			rate = self.BackgroundSpectrum(energy, "ER", "internal", self.detector.activeMass, -1) + \
					 self.BackgroundSpectrum(energy, "ER", "external", -1., self.detector.TPCArea)
		elif interaction=="NR" and signal=="S1" :
			rate =	self.BackgroundSpectrum(energy, "NR", "internal", self.detector.activeMass, -1) + \
					  self.BackgroundSpectrum(energy, "NR", "external", -1, self.detector.TPCArea)
		# Backgrounds relevant to lone-s2
		# The internal rate of ER and NR in fiducial mass + external rate on TPC area					   
		elif interaction=="ER" and signal=="S2":
			rate = self.BackgroundSpectrum(energy, "ER", "internal", self.detector.fiducialMass, -1) + \
					  self.BackgroundSpectrum(energy, "ER", "external", -1., self.detector.radius *	 self.detector.radius * np.pi)
		elif interaction=="NR" and signal=="S2":
			rate = self.BackgroundSpectrum(energy, "NR", "internal", self.detector.fiducialMass, -1) + \
					 self.BackgroundSpectrum(energy, "NR", "external", -1, self.detector.radius *  self.detector.radius * np.pi)

		return rate 
	''' CIV: charge insensitive volume. We have two contributions here: the internal backgrounds that
	go with the LXe mass in this volume, and external backgrounds that go with the area. We consider the
	area of the 'lid' though technically the PTFE sleeve here should be considered as well. '''	
	def BackgroundSpectrumFromCIV(self, energy, interaction):		
		rate = self.BackgroundSpectrum(energy, interaction, "internal", self.detector.S2BlindMass)  \
							+ self.BackgroundSpectrum(energy, interaction, "external", -1, self.detector.TPCLidArea)
		return rate


'''
This class stores parameters related to instrumental backgrounds, most notably the rate of 
lone S1 and lone S2 that cannot be explained by particle backgrounds. It also performs the calculations
related to a) coincidences between dark counts, b) the probability that all electrons from an interaction 
are absorbed, c) the probability that all photons from an interaction are absorbed.

ToDo: Small S2 misclassified as an S1

'''		
class InstrumentalBackground:
	def __init__(self,
				 detector,
				 A_unexplainedLoneS2,  # 1/yr per (area)
				 b1_unexplainedLoneS2,
				 b2_unexplainedLoneS2,
				 r_unexplainedLoneS2,
				 c_unexplainedLoneS2, # 1/yr per area
				 unexplainedLoneS1Rate, # HZ per (PTFE area) - FIXME; there is dependence on the rate of HE events that is not taken into account here
				 # This is a photon count rate not from dark noise. The rate fluctuates with distance in time to a previous event, but here
				 # we use some average rate left over after an assumed 'shadow cut'.
				 S1MisclassificationProb,
				 ): 
		self.detector = detector
		if detector is None:
			print("Class:InstrumentalBackground Error: Detector must not be None.") #Fixme, throw a proper error			
		self.A_unexplainedLoneS2 = A_unexplainedLoneS2 * SecondsPerYear * self.detector.TPCArea  # events/year
		self.b1_unexplainedLoneS2 = b1_unexplainedLoneS2
		self.b2_unexplainedLoneS2 = b2_unexplainedLoneS2	
		self.r_unexplainedLoneS2 = r_unexplainedLoneS2
		self.c_unexplainedLoneS2 = c_unexplainedLoneS2* SecondsPerYear * self.detector.TPCArea
		self.S1MisclassificationProb = S1MisclassificationProb
		self.unexplainedLoneS1Rate = unexplainedLoneS1Rate * (self.detector.TPCArea - self.detector.TPCLidArea) #multiply in only the area of the PTFE 
		
	def RUnexplainedS2(self, n):
		A = self.A_unexplainedLoneS2
		b1 = self.b1_unexplainedLoneS2
		b2 = self.b2_unexplainedLoneS2
		r = self.r_unexplainedLoneS2
		c = self.c_unexplainedLoneS2
		return	A*(r/b1 * np.exp(-n/b1) + (1-r)/b2 * np.exp(-n/b2)) + c
	
	def SESpectrum(self, n):
		# Fixme, we just model this as a gaussian for now, but should put in proper shape.
		# using a width half the mean is just eyeballed from the SE spectrum in XENONnT
		return Gaus(n, self.detector.SEGain, self.detector.SEGain/2.0)
		
	def DNCoincidenceRate(self, multiplicity, includeUnxeplainedLonePhotons=True):
		# Fixme, add the cut that requires that the hits are on different PMTs
		AllCountsToConsider = self.detector.TotalDNRate
		if includeUnxeplainedLonePhotons:
			AllCountsToConsider = AllCountsToConsider + self.unexplainedLoneS1Rate 
		ExpectedEventsInWindow = self.detector.S1CoincidenceWindow * AllCountsToConsider * 1e-9
			
		return AllCountsToConsider * PoissonV(ExpectedEventsInWindow,multiplicity-1) * SecondsPerYear 

	def P_ElectronLostByDrifttime(self, driftTime):
		return (1. - np.exp(-driftTime/self.detector.ElectronLifetime)) 
	
	def P_AllElectronsLost(self, startNumber, driftTime):
		pLostLifetime = self.P_ElectronLostByDrifttime(driftTime) 
		pLostg2 = (1.-self.detector.g2/self.detector.SEGain)  # Fixme; if g2 is lower than SEgain, it means electrons are lost while drifting. But this ratio is much bigger than what we'd lose just based on the electron lifetime
		pTotal = pLostLifetime + pLostg2*(1. -pLostLifetime) # We assume electrons can both be eaten by impurities, and get lost in other ways that reduce g2
		return np.power(pTotal, startNumber) # p^k = binomial probablity for number successes = number trials

	def P_PhotonNotDetected(self, event_height):
		m = (self.detector.LCETop - self.detector.LCEBottom)/self.detector.height 
		b = self.detector.LCEBottom
		return 1. - self.detector.PMTDetectionProb*(m*event_height + b) 
	
	#fixme - probability should be P(<1 or 2 phd) since those do not count as S1 
	def P_AllPhotonsLost(self, startNumber, event_height):
		pLost = self.P_PhotonNotDetected(event_height)
		return np.power(pLost, startNumber)
	
	''' electrons: Max original number of electrons to consider
		maxDriftTime: in ms'''
	def PlotElectronLossProbability(self, electrons=10, maxDriftTime=4):
		y_driftTime = np.linspace(1.3, maxDriftTime, 200)	#ms
		x_originalElectrons = np.linspace(1, electrons, electrons) #number electrons created
		X_originalElectrons, Y_driftTime = np.meshgrid(x_originalElectrons, y_driftTime)
		Z_ElectronLoss = self.P_AllElectronsLost(X_originalElectrons, Y_driftTime)
		fig_Btime, ax_Btime = plt.subplots()
		levels = np.ndarray((4,), buffer=np.array([1e-6, 1e-4, 1e-2, 0.1]))
		im = ax_Btime.pcolormesh(X_originalElectrons, Y_driftTime,	Z_ElectronLoss, norm=colors.LogNorm())
		#ax_Btime.contour(Y_B_ms, X_Btime_ms, Z_Btime, levels=levels, norm=colors.LogNorm(), cmap='Purples')
		ax_Btime.set_ylabel("Drift time [ms]")
		ax_Btime.set_xlabel("Original number of electrons")
		ax_Btime.set_title("Probability that all electrons got lost")
		fig_Btime.colorbar(im, ax=ax_Btime, pad=0.2, label="Probability")
		plt.show()


    
	def PlotDarkNoiseRate(self):
		x_DN = np.linspace(1, 5, 5)
		y_DNCoincidenceRate = self.DNCoincidenceRate(x_DN, False)
		y_DNAndUnexplainedCoincidenceRate = self.DNCoincidenceRate(x_DN, True)
		fig_DN, ax_DN = plt.subplots()
		legend=str(self.detector.PMTs) + " PMTs@" + str(self.detector.PMTDarkRate) + " Hz = " + "{:.1f}".format(self.detector.PMTs*self.detector.PMTDarkRate/1000) + "kHz; in " + str(self.detector.S1CoincidenceWindow) +" ns"
		legend2 = "Unexplained lone-S1 rate of " + "{:.1f}".format(self.unexplainedLoneS1Rate/1000) + "kHz"
		ax_DN.semilogy(x_DN, y_DNCoincidenceRate, linewidth=2.0, label=legend)
		ax_DN.semilogy(x_DN, y_DNAndUnexplainedCoincidenceRate, linewidth=2.0, label=legend2)
		ax_DN.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))
		ax_DN.grid()
		ax_DN.legend()
		ax_DN.set_xlabel("Nfold coincidence")
		ax_DN.set_ylabel("Events per year")
		ax_DN.set_title("Lone S1 from DN pile-up")
		plt.show()
		
		x_DN = np.linspace(1, 30, 30)
		y_ULS2 = self.RUnexplainedS2(x_DN)

		fig_SE, ax_SE = plt.subplots()
		ax_SE.semilogy(x_DN, y_ULS2, linewidth=2.0, label="Unexplained lone-S2 rate of " + "{:.2f}".format(self.A_unexplainedLoneS2/SecondsPerYear) + "Hz")		
		ax_SE.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))
		ax_SE.grid()
		ax_SE.legend()
		ax_SE.set_xlabel("Number of electrons")
		ax_SE.set_ylabel("Events per year")
		ax_SE.set_title("Unexplained lone S2")		
		plt.show()
		
	def PhotonLossProbability(self, photons=100):
	
		x_C2 = np.linspace(1, photons, photons) #number photons created
		y_C2 = np.linspace(1, int(self.detector.height), int(self.detector.height))
		X_C2, Y_C2 = np.meshgrid(x_C2, y_C2)
		Z_C2 = self.P_AllPhotonsLost(X_C2, Y_C2)

		fig_C2, ax_C2 = plt.subplots()
		levels = np.ndarray((6,), buffer=np.array([0.001, 0.01, 0.2, 0.4, 0.6, 0.8]))
		im = ax_C2.pcolormesh(X_C2, Y_C2,  Z_C2, cmap='plasma')
		ax_C2.contour(X_C2, Y_C2, Z_C2, levels=levels, norm=colors.LogNorm(), cmap='Purples')
		ax_C2.set_ylabel("Event height [cm]")
		ax_C2.set_xlabel("Original number of photons")
		ax_C2.set_title("Probability that all S1 photons got lost")
		fig_C2.colorbar(im, ax=ax_C2, label="Probability")
		plt.show()
		

	