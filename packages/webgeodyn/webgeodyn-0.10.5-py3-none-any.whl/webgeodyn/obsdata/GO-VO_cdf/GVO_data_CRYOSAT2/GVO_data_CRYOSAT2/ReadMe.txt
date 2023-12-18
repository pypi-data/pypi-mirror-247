Cryosat-2 GVO datafiles:

CR_OPER_VOBS_1M_2__20100815T000000_20181215T000000_0201.cdf
CR_OPER_VOBS_4M_2__20100701T000000_20181101T000000_0201.cdf
CR_OPER_VOBS_12M_2__20100701T000000_20180701T000000_0201.cdf

Variables:
Timestamp    - time in milliseconds since 01-Jan-0000 00:00:00.000 of B_OB and B_CF 
Latitude     - latitude in degrees of GVO
Longitude    - longitude in degrees of GVO
Radius       - radius in metres of GVO
B_OB         - observed field in nT
sigma_OB     - error estimate of observed field in nT
B_CF         - core field in nT
sigma_CF     - error estimate of core field in nT
Timestamp_SV - time in milliseconds since 01-Jan-0000 00:00:00.000 of B_SV
B_SV         - SV field in nT/yr
sigma_SV     - error estimate of SV field in nT/yr

%==========================================================================
Documentation: 

Ref 1): Swarm Geomagnetic Virtual Observatories Description of the Processing Algorithm, Rev. 3A, SW-DS-DTU-GS-005_2_GVO_DPA

Ref 2): Swarm Geomagnetic Virtual Observatories Product Definition, Rev.2B, SW-DS-DTU-GS-004_2-1_GVO_PDD

Ref 3): Olsen, N., Albini, G., Bouffard, J., Parrinello, T. and Tøffner-Clausen, L., 2020. 
	Magnetic observations from CryoSat-2: calibration and processing of satellite platform magnetometer data. 
	Earth, Planets and Space, 72(1), pp.1-18.
%==========================================================================
The GVO processing using the CRYOSAT-2 data are in accordance with Ref 1).
- GVO model setup:
    -300 globally distributed GVOs using an equal area grid (Leopardi 2006)
    -GVO data search range is 700km around each VO location
    -GVO data are collected for 1 or 4 or 12 months ad a time 
    -GVO altitudes are 727km 
    -Data along-track differences and sums are used
    -GVO fit using cubic potential description
    -Inversion limit = 30 data points
    -IGRF-13 used as main field model in processing
%==========================================================================
The GVO CRYOSAT 2 cdf files have a format in accordance with GVO Swarm cdf files described in Ref 2).

1) 1-month GVOs
    Data used:
    - CRYOSAT-2 CHAOS calibrated data Ref 3).
    - Down-sampled to 16 sec data sampling rate (Cryosat samples every 4 sec)
    - Flags: attitude quality flag q_flag < 40 
    - No data selection criteria applied
	
    B_OB: observed field time series
    - covers period: 2011-2018

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - PCA denoising applied.
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13.

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

2) 4-month GVOs
    Data used
    - CRYOSAT-2 CHAOS calibrated data Ref 3).
    - Down-sampled to 16 sec data sampling rate (Cryosat samples every 4 sec)
    - Flags: attitude quality flag q_flag < 40 
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizont
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
	
    B_OB: observed field time series
    - covers period: 2011-2018

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - Estimates of CIY4 ionopsheric and induced fields removed
    - Estimates of CHAOS-7.8 magnestospheric and induced fields removed
    - SHA denoising applied: external and toroidal terms estimated to SH degree 5 (degree 13 if 300 GVOs were available). At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

3) 12-month GVOs
    Data used
    - CRYOSAT-2 CHAOS calibrated data Ref 3).
    - Down-sampled to 16 sec data sampling rate (Cryosat samples every 4 sec)
    - Flags: attitude quality flag q_flag < 40 
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizont
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
	
    B_OB: observed field time series
    - covers period: 2011-2018

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - Estimates of CIY4 ionopsheric and induced fields removed
    - Estimates of CHAOS-7.8 magnestospheric and induced fields removed
    - SHA denoising applied: external and toroidal terms estimated to SH degree 5 (degree 13 if 300 GVOs were available). At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series
%==========================================================================

