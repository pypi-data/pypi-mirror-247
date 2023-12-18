CHAMP GVO datafiles:

CH_OPER_VOBS_1M_2__20000815T000000_20100915T000000_0201.cdf
CH_OPER_VOBS_4M_2__20000701T000000_20100701T000000_0201.cdf
CH_OPER_VOBS_12M_2__20000701T000000_20100701T000000_0201.cdf

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

Ref 3): GFZ Section 2.3 (2019): CHAMP: Overview of Final ME Products and Format Description,
	(Scientific Technical Report STR - Data; 19/10), Potsdam: GFZ German Research Centre for
	Geosciences. DOI: https://doi.org/10.2312/GFZ.b103-19104
%==========================================================================
The GVO processing using the CHAMP data are in accordance with the Ref 1).
- GVO model setup:
    -300 globally distributed GVOs using an equal area grid (Leopardi 2006)
    -GVO data search range is 700km around each GVO location
    -GVO data are collected for 1 or 4 or 12 months ad a time 
    -GVO altitudes are 370km during CHAMP period
    -Data along-track differences and sums are used
    -GVO fit using cubic potential description
    -Inversion limit = 30 data points
    -IGRF-13 used as main field model in processing
%==========================================================================
The GVO CHAMP cdf files have a format in accordance with GVO Swarm cdf files described in the Ref 2).

1) 1-month GVOs
    Data used:
    - CHAMP MAG-L3 data (available from https://isdc.gfz-potsdam.de/homepage/) 
    - Flags: the recommended flags listed in Ref 1), section 3.3.1 has been applied.
    - Down-sampled to 15 sec data sampling rate
    - No data selection criteria applied
	
    B_OB: observed field time series
    - covers period: 2000-2010

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - PCA denoising applied.
    - SHA denoising applied: external and toroidal terms estimated to SH degree 5 (degree 13 if 300 GVOs were available). At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

2) 4-month GVOs
    Data used
    - CHAMP MAG-L3 data (available from https://isdc.gfz-potsdam.de/homepage/) 
    - Flags: the recommended flags listed in Ref 1), section 3.3.1 has been applied.
    - Down-sampled to 15 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizont
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
	
    B_OB: observed field time series
    - covers period: 2000-2010

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - Estimates of CIY4 ionopsheric and induced fields removed
    - Estimates of CHAOS-7.8 magnestospheric and induced fields removed
    - SHA denoising applied: external and toroidal terms estimated to SH degree 5 (degree 13 if 300 GVOs were available). At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

3) 12-month GVOs
    Data used
    - CHAMP MAG-L3 data (available from https://isdc.gfz-potsdam.de/homepage/) 
    - Flags: the recommended flags listed in Ref 1), section 3.3.1 has been applied.
    - Down-sampled to 15 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizont
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
	
    B_OB: observed field time series
    - covers period: 2000-2010

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - Estimates of CIY4 ionopsheric and induced fields removed
    - Estimates of CHAOS-7.8 magnestospheric and induced fields removed
    - SHA denoising applied: external and toroidal terms estimated to SH degree 5 (degree 13 if 300 GVOs were available). At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series
%==========================================================================

