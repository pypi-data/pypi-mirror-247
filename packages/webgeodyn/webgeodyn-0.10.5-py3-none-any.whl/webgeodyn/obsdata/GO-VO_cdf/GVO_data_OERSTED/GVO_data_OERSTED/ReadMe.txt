Oersted GVO datafiles:

OR_OPER_VOBS_1M_2__19990415T000000_20050815T000000_0201.cdf
OR_OPER_VOBS_4M_2__19990301T000000_20051101T000000_0201.cdf
OR_OPER_VOBS_12M_2__19990701T000000_20050701T000000_0201.cdf

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
%==========================================================================
The GVO processing using Oersted data are in accordance with Ref 1).
- GVO model setup:
    -300 globally distributed GVOs using an equal area grid (Leopardi 2006)
    -GVO data search range is 700km around each VO location
    -GVO data are collected for 1 or 4 months ad a time 
    -Data along-track differences and sums are used
    -GVO fit using cubic potential description
    -Inversion limit = 20 data points
    -IGRF-13 used as main field model in processing

    -For Oersted GVOs the error estimates are computed as: 
    ->sigma_CF error estimates of the GVO CORE field are computed based on the residuals towards internal CHAOS-7.8 field predictions (deg 1-20).
     The residuals are computed for two latitude bands: a) 50N-90N degrees together with 50S-90S degrees and b) 50S-50N deg.
     Using all residual within each band, the error estimates are computed as the square root of the residual robust mean squared plus the residual robust standard deviation squared.

    ->sigma_SV error estimates of the GVO SV field are computed based on the residuals towards internal CHAOS-7.8 field predictions (deg 1-20).
     The residuals are computed for two latitude bands: a) 50N-90N degrees together with 50S-90S degrees and b) 50S-50N deg.
     Using all residual within each band, the error estimates are computed as the square root of the residual robust mean squared plus the residual robust standard deviation squared.
%==========================================================================
The GVO composite cdf files have a format in accordance with GVO Swarm cdf files described in Ref 2).

1) 1-month GVOs
    Data used:
    - Oersted data (available from ftp://ftp.spacecenter.dk/data/magnetic-satellites/Oersted/)
    - Down-sampled to 15 sec data sampling rate
    - No data selection criteria applied
	
    B_OB: observed field time series
    - covers period: 1999-2005

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - PCA denoising applied.
    - SHA denoising applied: No SHA denoising applied to Oersted data. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

2) 4-month GVOs
    Data used
    - Oersted data (available from ftp://ftp.spacecenter.dk/data/magnetic-satellites/Oersted/)
    - Down-sampled to 15 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizon
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
	
    B_OB: observed field time series
    - covers period: 1999-2005

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - Estimates of CIY4 ionospheric and induced fields removed
    - Estimates of CHAOS-7.8 magnestospheric and induced fields removed
    - SHA denoising applied: No SHA denoising applied to Oersted data. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

3) 12-month GVOs
    Data used
    - Oersted data (available from ftp://ftp.spacecenter.dk/data/magnetic-satellites/Oersted/)
    - Down-sampled to 15 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizon
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
	
    B_OB: observed field time series
    - covers period: 1999-2005

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - Estimates of CIY4 ionospheric and induced fields removed
    - Estimates of CHAOS-7.8 magnestospheric and induced fields removed
    - SHA denoising applied: No SHA denoising applied to Oersted data. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series
%==========================================================================
*NOTE: High scatter level in the Oersted GVO time series are seen.  Likely due anisotropic errors, there can be large outliers.  Please beware if using Gaussian statistics.

