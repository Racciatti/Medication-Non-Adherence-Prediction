# nhanes_data_dictionary.md

This technical data dictionary defines the specific variables selected from the NHANES 2013-2014 (Cycle H) modules for analysis. Technical descriptions are derived exclusively from official NHANES questionnaire, dietary, and demographic documentation[cite: 1, 2, 3].

---

## 1. Demographics Module (`DEMO_H.xpt`)
Contains individual-level demographic and socioeconomic data points used for sample stratification and weighting[cite: 3].

| Variable | Description | Source |
| :--- | :--- | :--- |
| **SEQN** | Respondent sequence number |[cite: 3] |
| **RIDAGEYR** | Age in years at screening (topcoded at 80 years) |[cite: 3] |
| **RIAGENDR** | Gender of the participant |[cite: 3] |
| **DMDEDUC2** | Highest level of education completed (Adults 20+) |[cite: 3] |
| **DMDMARTL** | Marital status of the participant |[cite: 3] |
| **DMDFMSIZ** | Total number of people in the NHANES family |[cite: 3] |
| **DMDHHSIZ** | Total number of people in the household |[cite: 3] |
| **DMDHHSZA** | Number of children aged 5 years or younger in the household |[cite: 3] |
| **DMDHHSZB** | Number of children aged 6–17 years old in the household |[cite: 3] |
| **DMDHHSZE** | Number of adults aged 60 years or older in the household |[cite: 3] |
| **DMDHRAGE** | Household reference person's age in years |[cite: 3] |
| **DMDHRGND** | Household reference person's gender |[cite: 3] |
| **DMDHREDU** | Household reference person's education level |[cite: 3] |
| **DMDHSEDU** | Household reference person's spouse's education level |[cite: 3] |
| **DMDHRMAR** | Household reference person's marital status |[cite: 3] |
| **INDFMIN2** | Total annual family income (reported as a range value) |[cite: 3] |
| **INDHHIN2** | Total annual household income (reported as a range value) |[cite: 3] |

---

## 2. Dietary Intake Modules (`DR1TOT_H.xpt`, `DR2TOT_H.xpt`)
Captures technical nutrient intake and special dietary adherence data over two 24-hour recall periods[cite: 2].

| Variable | Technical Description | Source |
| :--- | :--- | :--- |
| **DR1_320Z** | Total grams of plain water drank (Day 1) |[cite: 2] |
| **DR2_320Z** | Total grams of plain water drank (Day 2) |[cite: 2] |
| **DR1DRSTZ** | Dietary recall status/reliability (Day 1) |[cite: 2] |
| **DR2DRSTZ** | Dietary recall status/reliability (Day 2) |[cite: 2] |
| **DR1TALCO** | Total alcohol intake in grams (Day 1) |[cite: 2] |
| **DR2TALCO** | Total alcohol intake in grams (Day 2) |[cite: 2] |
| **DR1TCAFF** | Total caffeine intake in milligrams (Day 1) |[cite: 2] |
| **DR2TCAFF** | Total caffeine intake in milligrams (Day 2) |[cite: 2] |
| **DR1TKCAL** | Total energy intake in kilocalories (Day 1) |[cite: 2] |
| **DR2TKCAL** | Total energy intake in kilocalories (Day 2) |[cite: 2] |
| **DR1TPROT** | Total protein intake in grams (Day 1) |[cite: 2] |
| **DR2TPROT** | Total protein intake in grams (Day 2) |[cite: 2] |
| **DR1TSUGR** | Total sugar intake in grams (Day 1) |[cite: 2] |
| **DR2TSUGR** | Total sugar intake in grams (Day 2) |[cite: 2] |
| **DR1TTFAT** | Total fat intake in grams (Day 1) |[cite: 2] |
| **DR2TTFAT** | Total fat intake in grams (Day 2) |[cite: 2] |
| **DRQSDIET** | Binary indicator: Currently on any kind of diet? |[cite: 2] |
| **DRQSDT1–12** | Specific diet type flags (e.g., weight loss, low fat, diabetic) |[cite: 2] |
| **DRQSDT91** | Adherence to "another type" of special diet |[cite: 2] |

---

## 3. Dietary Supplement Modules (`DS1TOT_H.xpt`, `DS2TOT_H.xpt`)
Total supplemental nutrient intake aggregated across all reported supplements[cite: 2].

| Variable | Description | Source |
| :--- | :--- | :--- |
| **DS1TCALC** | Total calcium from supplements in milligrams (Day 1) |[cite: 2] |
| **DS2TCALC** | Total calcium from supplements in milligrams (Day 2) |[cite: 2] |
| **DS1TCAFF** | Total caffeine from supplements in milligrams (Day 1) |[cite: 2] |
| **DS2TCAFF** | Total caffeine from supplements in milligrams (Day 2) |[cite: 2] |

---

## 4. Physical Activity Module (`PAQ_H.xpt`)
Metric tracking for occupational, transport-related, and leisure activities[cite: 1].

| Variable | Description | Source |
| :--- | :--- | :--- |
| **PAQ635** | Walk or bicycle for travel at least 10 minutes continuously |[cite: 1] |
| **PAQ640** | Days per week walked or bicycled for travel |[cite: 1] |
| **PAD645** | Minutes per day spent walking or bicycling for travel |[cite: 1] |
| **PAQ679** | Minutes think you should be active for good health |[cite: 1] |
| **PAQ678** | Days exercises to strengthen/tone muscles in past 7 days |[cite: 1] |
| **PAQ677** | Days exercise 20+ mins causing sweat/hard breathing (past 7) |[cite: 1] |
| **PAQ650** | Engagement in vigorous-intensity sports/fitness activities |[cite: 1] |
| **PAQ655** | Days per week doing vigorous sports/fitness |[cite: 1] |
| **PAD660** | Typical daily minutes of vigorous sports/fitness |[cite: 1] |
| **PAQ665** | Engagement in moderate-intensity sports/fitness activities |[cite: 1] |
| **PAQ670** | Days per week doing moderate sports/fitness |[cite: 1] |
| **PAD675** | Typical daily minutes of moderate sports/fitness |[cite: 1] |
| **PAD680** | Minutes spent sitting on a typical day (excluding sleep) |[cite: 1] |
| **PAQ731** | Days played active video games in past 7 days |[cite: 1] |
| **PAQ715** | Daily hours of computer use outside of school/work |[cite: 1] |
| **PAQ710** | Daily hours spent watching TV or videos |[cite: 1] |
| **PAQ706** | Days active 60+ mins per day (Ages 12–17) |[cite: 1] |

---

## 5. Physical Functioning & Disability (`PFQ_H.xpt`, `DLQ_H.xpt`)
Functional capacity assessments and long-term limitation indicators[cite: 1].

| Variable | Technical Description | Source |
| :--- | :--- | :--- |
| **PFQ059** | Limited in any activity due to physical/mental/emotional problem |[cite: 1] |
| **PFQ057** | Limited due to confusion or periods of difficulty remembering |[cite: 1] |
| **PFQ054** | Difficulty walking without the use of special equipment |[cite: 1] |
| **PFQ061H** | Difficulty walking room-to-room on the same level |[cite: 1] |
| **PFQ061I** | Difficulty standing up from an armless straight chair |[cite: 1] |
| **PFQ061P** | Difficulty using fingers to grasp or handle small objects |[cite: 1] |
| **PFQ061J** | Difficulty getting in or out of bed |[cite: 1] |
| **PFQ061K** | Difficulty eating (e.g., holding fork, drinking from glass) |[cite: 1] |
| **DLQ010** | Binary indicator: Deaf or serious difficulty hearing? |[cite: 1] |
| **DLQ020** | Binary indicator: Blind or serious difficulty seeing (with glasses)? |[cite: 1] |
| **DLQ040** | Difficulty concentrating, remembering, or making decisions |[cite: 1] |
| **DLQ050** | Difficulty walking or climbing stairs |[cite: 1] |

---

## 6. Behavioral & Clinical Indicators
Captures substance use, healthcare access, and medical condition history[cite: 1].

### Alcohol Use (`ALQ_H.xpt`)
| Variable | Technical Description | Source |
| :--- | :--- | :--- |
| **ALQ120Q** | Frequency of alcohol consumption in the past 12 months |[cite: 1] |
| **ALQ120U** | Unit of measure for ALQ120Q (Week, Month, Year) |[cite: 1] |
| **ALQ130** | Average alcoholic drinks per day on drinking days |[cite: 1] |
| **ALQ141Q** | Frequency of heavy drinking (4/5+ drinks) in the past year |[cite: 1] |
| **ALQ141U** | Unit of measure for heavy drinking frequency |[cite: 1] |

### Consumer Behavior (`CBQ_H.xpt`)
| Variable | Technical Description | Source |
| :--- | :--- | :--- |
| **CBD120** | Money spent on eating out in the past 30 days |[cite: 1] |
| **CBD070** | Money spent at supermarkets or grocery stores in past 30 days |[cite: 1] |

### Access to Care (`HUQ_H.xpt`)
| Variable | Technical Description | Source |
| :--- | :--- | :--- |
| **HUQ051** | Frequency of visits to healthcare professionals in past 12 months |[cite: 1] |
| **HUQ061** | Time elapsed since last saw or talked to a doctor |[cite: 1] |

### Osteoporosis & Medical Conditions (`OSQ_H.xpt`, `MCQ_H.xpt`)
| Variable | Technical Description | Source |
| :--- | :--- | :--- |
| **OSQ072** | Ever told by a doctor to take medicine for osteoporosis |[cite: 1] |
| **OSQ060** | Ever told by a doctor that you had osteoporosis |[cite: 1] |
| **MCQ084** | Confusion or memory loss worsening in the past 12 months |[cite: 1] |

---

## 7. Socioeconomic, Medication, & Sleep Modules
Metadata for income, prescription usage, and sleep duration[cite: 1].

| Variable | Module | Technical Description | Source |
| :--- | :--- | :--- | :--- |
| **INQ244** | `INQ_H` | Savings/Checking accounts total more than $5,000 |[cite: 1] |
| **IND235** | `INQ_H` | Total monthly family income range |[cite: 1] |
| **IND247** | `INQ_H` | Family income from wages, salaries, or tips |[cite: 1] |
| **SLD010H** | `SLQ_H` | Hours of sleep per night on weekdays/workdays |[cite: 1] |
| **RXDCOUNT**| `RXQ_RX_H` | Total number of prescription medicines reported |[cite: 1] |

---

## 8. Linkage Only Modules
The following modules are loaded for primary key synchronization; only the identifier is currently utilized.

*   **Blood Pressure & Cholesterol (`BPQ_H.xpt`)**: Contains self-reported hypertension data[cite: 1].
*   **Diabetes (`DIQ_H.xpt`)**: Contains self-reported diabetic status data[cite: 1].