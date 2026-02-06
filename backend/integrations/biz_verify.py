def verify_biz_registration(biz_reg_no: str) -> bool:
    # TODO: Replace with real 사업자번호 검증 API integration.
    # For now, accept non-empty values as valid.
    return bool(biz_reg_no and biz_reg_no.strip())
