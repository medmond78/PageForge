# FDA CSA Roadmap for ANSYS Mechanical
## Implementation Sequence for Software Validation

---

## Phase 1: Foundation & Assessment (Weeks 1-2)

### 1.1 Define Intended Use
**What:** Document how ANSYS will be used in production/QMS  
**Why:** FDA CSA validation is tied to specific intended use - different uses = different risk = different validation rigor

**Deliverable:** Clear statement like:
> "ANSYS Mechanical is used to predict mechanical performance of PFS designs to support design verification documented in DHF and regulatory submissions. Results are reviewed by qualified engineer and confirmed by physical testing."

### 1.2 Determine Process Risk Classification
**What:** Assess if ANSYS poses "high process risk" or "not high process risk"  
**Why:** Determines validation rigor - high risk = detailed scripted testing; not high = exploratory testing

**Key Question:** If ANSYS fails, does it result in quality problem that foreseeably compromises safety?

**Deliverable:** Process risk determination with rationale

### 1.3 Determine Model Risk (ASME V&V40)
**What:** Calculate Model Influence × Decision Consequence → Model Risk  
**Why:** Parallel assessment to FDA CSA - determines credibility evidence needed (MC/PQ sections)

**Deliverable:** Model risk level (Low/Medium/High) from V&V40 worksheet

---

## Phase 2: Vendor Assessment (Week 3)

### 2.1 ANSYS Vendor Evaluation
**What:** Assess ANSYS Inc.'s capabilities, certifications, development practices  
**Why:** FDA CSA encourages leveraging vendor validation work - strong vendor = less you need to do

**Activities:**

- Review ANSYS quality management system
- Review ANSYS software development lifecycle
- Review ANSYS verification/validation documentation
- Review relevant certifications (ISO 9001, etc.)

**Deliverable:** Vendor assessment report per purchasing controls SOP

### 2.2 Determine What to Leverage
**What:** Decide which ANSYS validation work you can leverage vs. what you need to supplement  
**Why:** Avoid duplicating vendor's work - focus your effort on your specific intended use

**Deliverable:** Gap analysis (vendor provides X, we need to supplement with Y)

---

## Phase 3: Validation Planning (Week 4)

### 3.1 Determine Assurance Activities
**What:** Select testing methods based on process risk and model risk  
**Why:** Right-size validation effort - proportional to risk

**High Process Risk → Scripted testing, detailed protocol**  
**Not High Process Risk → Exploratory testing, summary documentation**

**Activities:**

- Define IQ checks (installation verification)
- Define OQ benchmarks (operational verification - cantilever, pressure vessel, etc.)
- Define MC approach (mesh convergence study)
- Define PQ validation (physical test correlation)

**Deliverable:** Validation plan section in qualification protocol

### 3.2 Define Acceptance Criteria
**What:** Quantitative pass/fail criteria for each validation activity  
**Why:** Objective evidence requires objective criteria

**Examples:**

- IQ: All checks PASS
- OQ: Benchmark errors <5% (per credibility table)
- MC: GCI <1%, <5% change between finest meshes
- PQ: Bias <15%, within 95% CI (for Medium Risk)

**Deliverable:** Acceptance criteria table

---

## Phase 4: Installation & Configuration (Week 5)

### 4.1 ANSYS Installation (IQ)
**What:** Install ANSYS, verify hardware/software specifications  
**Why:** Establishes baseline - software installed correctly per vendor specs

**Activities:**

- Install ANSYS Mechanical (specific version)
- Verify system requirements (RAM, CPU, GPU, OS)
- Verify license configuration
- Verify solver settings
- Document installation details

**Deliverable:** IQ section completed with pass/fail results

---

## Phase 5: Operational Qualification (Week 6)

### 5.1 Benchmark Testing (OQ)
**What:** Run analytical benchmark problems, compare to known solutions  
**Why:** Verifies ANSYS calculates correctly for physics relevant to your applications

**Recommended Benchmarks for PFS:**

1. **Cantilever beam** (bending - springs, needles)
2. **Thin-wall pressure vessel** (hoop stress - drug containers)
3. **Hertzian contact** (contact stress - plunger-stopper)
4. **Stress concentration** (notch factor - fillets, threads)

**Deliverable:** OQ section with benchmark results, % error calculations, pass/fail

---

## Phase 6: Mesh Convergence (Week 7)

### 6.1 Mesh Convergence Study (MC)
**What:** Run representative analysis with progressively finer meshes  
**Why:** Demonstrates solution is mesh-independent (calculation verification per ASME V&V40)

**Activities:**

- Select representative model (e.g., PFS under internal pressure)
- Run 4-5 mesh levels (coarse to fine)
- Calculate % change between meshes
- Calculate Grid Convergence Index (GCI)
- Select operational mesh (balance accuracy vs. solve time)

**Deliverable:** MC section with convergence data, GCI, mesh selection rationale

---

## Phase 7: Performance Qualification (Weeks 8-9)

### 7.1 Physical Test Correlation (PQ)
**What:** Compare ANSYS predictions to physical test data  
**Why:** Validates model accuracy for your specific application (validation per ASME V&V40)

**Activities:**

- Identify available physical test data (burst, pullout, drop, etc.)
- Run ANSYS models matching test conditions
- Calculate bias (FEA vs. test)
- Statistical analysis (95% confidence intervals)
- Assess conservative direction (over-prediction preferred)

**Deliverable:** PQ section with FEA-to-test comparison, bias analysis, pass/fail

---

## Phase 8: Documentation (Week 10)

### 8.1 Complete Qualification Report
**What:** Populate all sections of qualification template  
**Why:** Evidence of validation - required for ISO 13485, inspections

**Sections:**

1. Purpose, Scope, Regulatory Basis
2. Roles & Responsibilities
3. **Intended Use** (FDA CSA requirement)
4. Software Description
5. **Risk Assessment** (FDA CSA process risk + ASME V&V40 model risk)
6. IQ Results
7. OQ Results
8. MC Results
9. PQ Results
10. Traceability Matrix
11. Conclusion

**Deliverable:** Complete qualification report (SV-ANSYS-003 or similar)

### 8.2 Establish Electronic Records
**What:** Define how validation evidence will be stored/maintained  
**Why:** 21 CFR Part 11 compliance if records are electronic

**FDA CSA Recommendation:** Use system logs, audit trails, ANSYS project files (preferred over paper/screenshots)

**Deliverable:** Electronic records approach documented

---

## Phase 9: Review & Approval (Week 11)

### 9.1 Technical Review
**What:** Engineering Manager reviews qualification report  
**Why:** Independent verification of validation adequacy

**Deliverable:** Technical review sign-off

### 9.2 Quality Review
**What:** QA Manager reviews for compliance with procedures, regulations  
**Why:** Ensures regulatory compliance before final approval

**Deliverable:** QA review sign-off

### 9.3 Final Approval
**What:** System Owner approves qualification report  
**Why:** Establishes validated state - ANSYS authorized for production use

**Deliverable:** Approved qualification report, added to DHF and controlled documents

---

## Phase 10: Deployment & Maintenance (Ongoing)

### 10.1 Training
**What:** Train engineers on qualified ANSYS use  
**Why:** Qualified software must be used within validated scope

**Deliverable:** Training records, competency assessments

### 10.2 Change Management
**What:** Define process for ANSYS version updates, new applications  
**Why:** Maintain validated state throughout lifecycle

**Triggers for Re-Qualification:**

- New ANSYS version with solver changes
- New physics modules not covered by original qualification
- New applications outside validated domain (e.g., new device type, new materials)

**May NOT Require Re-Qualification:**

- ANSYS version with only GUI changes
- Same PFS type, different size
- Same materials, different geometry within envelope

**Deliverable:** Change management procedure

### 10.3 Periodic Review
**What:** Annual review of ANSYS qualification  
**Why:** Ensure continued fitness for intended use

**Activities:**

- Review any issues/deviations from past year
- Review adequacy of current qualification scope
- Determine if updates needed

**Deliverable:** Annual review record

---

## Critical Success Factors

### Dependencies

1. **Phase 2 before Phase 3** - Must know what vendor provides before planning your validation
2. **Phase 3 before Phase 5-7** - Must have acceptance criteria defined before testing
3. **Phases 5-7 before Phase 8** - Must have results before documenting them

### Resources Needed

- **Personnel:** Qualified engineer (run ANSYS), QA support (documentation)
- **Hardware:** ANSYS-capable workstation (already have)
- **Physical Test Data:** Historical data acceptable if representative
- **Time:** ~11 weeks for initial qualification (subsequent updates faster)

### Risk Mitigation

- **Gap:** No physical test data → Use conservative assumptions, acknowledge limitation in PQ
- **Gap:** Limited vendor access → Focus on publicly available documentation, industry standards
- **Gap:** Complex geometry → Start with simple representative model for MC/PQ

---

## Expected Outcomes

**Upon Completion:**

- ✓ ANSYS Mechanical validated per FDA CSA and ASME V&V40
- ✓ Documented evidence meeting ISO 13485 requirements
- ✓ Inspection-ready qualification report in DHF
- ✓ Clear intended use and risk classification
- ✓ Objective acceptance criteria and pass/fail results
- ✓ Change management process for future updates
- ✓ Engineers authorized to use ANSYS for design verification

**Regulatory Benefit:**

- Supports DIR verification (e.g., burst pressure, pullout force)
- Provides computational evidence for DHF
- Enables regulatory submissions with FEA data
- Demonstrates QMS compliance (21 CFR 820, ISO 13485)

---

## Key Takeaway

**Two parallel qualification tracks:**

1. **FDA CSA** → Software validation (Is the tool working?) → IQ/OQ
2. **ASME V&V40** → Model credibility (Is the model accurate?) → MC/PQ

**Both required. Both in one qualification report. ~11 weeks to validated state.**
