Swarm GVO datafiles:

SW_OPER_VOBS_1M_2__20131215T000000_20230515T000000_0201.cdf
SW_DTUJ_VOBS_4M_2_20140301T000000_20230301T000000_0201.cdf
SW_DTUJ_VOBS_12M_2_20140701T000000_20220701T000000_0201.cdf

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

Notes:
The 1 month data file included here is the official Swarm data product released, since this relies on the BGS PCA removal of external signals
The 4 month and 12 month files were produced by DTU in August 2023, using their software which was the prototype for the ESA 4 month data product.  The DTU 4 month product used more deta and a more recent RC versions for magnetospheric corrections, so is therefore prefer to the available Swarm operational product from May 2023. 

%==========================================================================
Documentation: 

Ref 1): Swarm Geomagnetic Virtual Observatories Description of the Processing Algorithm, Rev. 3A, SW-DS-DTU-GS-005_2_GVO_DPA

Ref 2): Swarm Geomagnetic Virtual Observatories Product Definition, Rev.2B, SW-DS-DTU-GS-004_2-1_GVO_PDD
%==========================================================================
The GVO processing using the Swarm data are in accordance with Ref 1).
- GVO model setup:
    -300 globally distributed GVOs using an equal area grid (Leopardi 2006)
    -GVO data search range is 700km around each VO location
    -GVO data are collected for 1 or 4 or 12 months ad a time 
    -GVO altitudes are 490km during Swarm period
    -Data along-track differences and sums are used
    -GVO fit using cubic potential description
    -Inversion limit = 30 data points
    -IGRF-13 used as main field model in processing
%==========================================================================
The GVO Swarm cdf files have a format in accordance with GVO Swarm cdf files described in Ref 2).

1) 1-month GVOs
    Data used:
    - Swarm Level 1b data, SW_OPER_MAGX_LR_1B, versions 0602 up to end of April 2023
    - Down-sampled to 15 sec data sampling rate
    - No data selection criteria applied
	
    B_OB: observed field time series
    - covers period: 2014-2023

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - PCA denoising applied.
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

2) 4-month GVOs
    Data used
    - Swarm Level 1b data, SW_OPER_MAGX_LR_1B, version 0602 up until end April 2023
    - Down-sampled to 15 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizon
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
    	- Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    	- Estimates of CIY4 ionopsheric and induced fields removed
        - Estimates of CHAOS-7.15 magnestospheric and induced fields removed
	
    B_OB: observed field time series
    - covers period: 2014-2023
	
    B_CF: core field time series
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13. At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series


3) 12-month GVOs
    Data used
    - Swarm Level 1b data, SW_OPER_MAGX_LR_1B, versions 0602 up until end of 2022
    - Down-sampled to 15 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizon
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
    	- Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    	- Estimates of CIY4 ionopsheric and induced fields removed
        - Estimates of CHAOS-7.15 magnestospheric and induced fields removed
	
    B_OB: observed field time series
    - covers period: 2014-2022

    B_CF: core field time series
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13. At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series
%==========================================================================

