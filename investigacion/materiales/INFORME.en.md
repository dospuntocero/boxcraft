[Español](INFORME.md) · English

# REA materials review — October 16, 2026

Status: partial; local changes, unpublished. Original materials are retained for all eleven boxes, and 64 additional measured configurations are enabled across ten boxes.

Observations: responses contain resulting geometry and internal/external allowances. The science field retains the original material in certain responses; effective selection is obtained from layer.traditional.science_id and layer.traditional.thickness. Changing dimensions can automatically replace the material or adjust advanced parameters, so paths cannot be attributed to the requested selection without checking the result.

Limitations: captures with incomplete closure were retained as partial observations. Only complete captured geometric responses are used; successful session closure is not claimed. The source returned 403 for /projects and /modes/category/cal; controls became disabled and subsequent captures provided no valid variations. This restriction was not bypassed.

Results not enabled: the affine dimension fit and continuous thickness fit failed validation; topology changes, rounding, and additional parameters are present. New configurations are limited to exact captured dimensions. Compatibility is not generalized from equal thickness or overlapping catalog ranges.

Coverage and evidence chain: collected.json links each response file to its capture and reference; observed-profile-ledger.json lists enabled cases. The *-result.json and retained-audit-final.json files contain complete or partial REA captures. profile-build-report.json and physical-fit-findings.md document rejected fits.

Validation: 56 Node tests passed; 75 enabled combinations were exercised through the interface with no error messages, no empty blanks, and downloading enabled. Automated checking of download events did not complete; downloaded-file verification is not claimed.

Pending: complete alternatives for 12109002, complete each box's matrix of other materials/thicknesses, and reconstruct variable-dimension behavior for new materials without extrapolating samples.
