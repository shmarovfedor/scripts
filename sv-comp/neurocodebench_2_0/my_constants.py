BENCHMARKS_WITH_MATH = ["tanh_w64_r1_case_0_unsafe","tanh_w64_r2_case_1_unsafe","tanh_w64_r2_case_0_safe","tanh_w64_r4_case_1_safe","tanh_w64_r1_case_1_safe","tanh_w64_r3_case_0_safe","tanh_w64_r4_case_0_safe","tanh_w64_r3_case_1_safe","tanh_w16_r2_case_0_safe","tanh_w16_r2_case_1_unsafe","tanh_w16_r1_case_1_safe","tanh_w16_r3_case_0_safe","tanh_w16_r1_case_0_unsafe","tanh_w16_r4_case_1_safe","tanh_w16_r4_case_0_safe","tanh_w16_r3_case_1_safe","tanh_w32_r1_case_1_safe","tanh_w32_r3_case_0_safe","tanh_w32_r2_case_1_unsafe","tanh_w32_r2_case_0_safe","tanh_w32_r3_case_1_safe","tanh_w32_r1_case_0_unsafe","tanh_w32_r4_case_1_safe","tanh_w32_r4_case_0_safe","tanh_w8_r4_case_0_safe","tanh_w8_r2_case_0_safe","tanh_w8_r1_case_1_safe","tanh_w8_r3_case_0_safe","tanh_w8_r3_case_1_unsafe","tanh_w8_r1_case_0_unsafe","tanh_w8_r4_case_1_unsafe","tanh_w8_r2_case_1_unsafe","tanh_w4_r3_case_0_safe","tanh_w4_r4_case_0_safe","tanh_w4_r4_case_1_unsafe","tanh_w4_r2_case_1_unsafe","tanh_w4_r2_case_0_safe","tanh_w4_r3_case_1_unsafe","tanh_w4_r1_case_1_safe","tanh_w4_r1_case_0_unsafe","softmax_3_unsafe","softmax_5_unsafe","softmax_13_unsafe","softmax_11_safe","softmax_6_safe","softmax_10_safe","softmax_9_unsafe","softmax_12_unsafe","softmax_0_safe","softmax_8_safe","softmax_4_safe","softmax_1_unsafe","softmax_2_safe","softmax_7_unsafe","layernorm_1_safe","layernorm_2_safe","layernorm_5_unsafe","layernorm_4_unsafe","layernorm_7_unsafe","layernorm_9_safe","layernorm_8_unsafe","layernorm_10_unsafe","layernorm_0_safe","layernorm_11_safe","layernorm_6_unsafe","layernorm_3_safe","batchnorm_6_safe","batchnorm_5_unsafe","batchnorm_11_unsafe","batchnorm_10_safe","batchnorm_3_unsafe","batchnorm_7_unsafe","batchnorm_9_safe","batchnorm_4_safe","batchnorm_2_safe","batchnorm_0_safe","batchnorm_8_safe","batchnorm_1_unsafe","expm1_1_safe","expm1_2_safe","expm1_6_safe","expm1_4_unsafe","expm1_0_safe","expm1_3_unsafe","expm1_5_unsafe","sin_3_unsafe","sin_4_safe","sin_2_safe","sin_5_unsafe","sin_6_safe","sin_7_safe","sin_0_safe","sin_1_safe","erf_0_safe","erf_3_unsafe","erf_2_safe","erf_5_safe","erf_1_safe","erf_4_safe","log_0_safe","log_2_safe","log_6_safe","log_4_safe","log_3_unsafe","log_5_unsafe","log_1_safe","log1p_0_safe","log1p_3_unsafe","log1p_5_unsafe","log1p_6_safe","log1p_1_safe","log1p_2_safe","log1p_4_safe","exp_1_safe","exp_6_safe","exp_0_safe","exp_3_safe","exp_5_unsafe","exp_4_unsafe","exp_2_safe","cos_0_safe","cos_7_safe","cos_2_safe","cos_5_unsafe","cos_3_unsafe","cos_6_safe","cos_4_safe","cos_1_safe","sqrt_4_unsafe","sqrt_5_safe","sqrt_7_safe","sqrt_6_unsafe","sqrt_0_safe","sqrt_2_safe","sqrt_1_safe","sqrt_3_safe","glu_5_unsafe","glu_3_unsafe","glu_2_safe","glu_4_safe","glu_0_safe","glu_1_safe","gelu_5_unsafe","gelu_4_unsafe","gelu_1_safe","gelu_3_unsafe","gelu_2_safe","gelu_0_safe","softplus_4_unsafe","softplus_1_safe","softplus_5_safe","softplus_2_safe","softplus_0_safe","softplus_3_safe","logistic_2_safe","logistic_4_safe","logistic_6_safe","logistic_7_unsafe","logistic_3_safe","logistic_5_unsafe","logistic_0_safe","logistic_1_safe","elu_1_safe","elu_0_safe","elu_2_safe","elu_4_safe","elu_3_unsafe","tanh_6_safe","tanh_0_safe","tanh_1_safe","tanh_4_safe","tanh_5_unsafe","tanh_3_safe","tanh_2_safe","tanh_7_safe","gaussian_4_safe","gaussian_0_safe","gaussian_2_safe","gaussian_3_unsafe","gaussian_1_safe"]

SAT_RELU_SAFE_ORDERED = ["prop_bool_v5_c5_safe", "prop_bool_v5_c10_safe", "prop_bool_v5_c15_safe", "prop_bool_v5_c20_safe", "prop_bool_v5_c25_safe", "prop_bool_v5_c30_safe", "prop_bool_v8_c8_safe", "prop_bool_v8_c16_safe", "prop_bool_v8_c24_safe", "prop_bool_v8_c32_safe", "prop_bool_v8_c40_safe", "prop_bool_v8_c48_safe", "prop_bool_v13_c13_safe", "prop_bool_v13_c26_safe", "prop_bool_v13_c39_safe", "prop_bool_v13_c52_safe", "prop_bool_v13_c65_safe", "prop_bool_v13_c78_safe", "prop_bool_v21_c21_safe", "prop_bool_v21_c42_safe", "prop_bool_v21_c63_safe", "prop_bool_v21_c84_safe", "prop_bool_v21_c105_safe", "prop_bool_v21_c126_safe", "prop_bool_v34_c34_safe", "prop_bool_v34_c68_safe", "prop_bool_v34_c102_safe", "prop_bool_v34_c136_safe", "prop_bool_v34_c170_safe", "prop_bool_v34_c204_safe", "prop_bool_v55_c55_safe", "prop_bool_v55_c110_safe", "prop_bool_v55_c165_safe", "prop_bool_v55_c220_safe", "prop_bool_v55_c275_safe", "prop_bool_v55_c330_safe", "prop_bool_v89_c89_safe", "prop_bool_v89_c178_safe", "prop_bool_v89_c267_safe", "prop_bool_v89_c356_safe", "prop_bool_v89_c445_safe", "prop_bool_v89_c534_safe", "prop_bool_v144_c144_safe", "prop_bool_v144_c288_safe", "prop_bool_v144_c432_safe", "prop_bool_v144_c576_safe", "prop_bool_v144_c720_safe", "prop_bool_v144_c864_safe"]

SAT_RELU_UNSAFE_ORDERED = ["prop_bool_v5_c5_unsafe", "prop_bool_v5_c10_unsafe", "prop_bool_v5_c15_unsafe", "prop_bool_v5_c18_unsafe", "prop_bool_v5_c24_unsafe", "prop_bool_v5_c27_unsafe", "prop_bool_v8_c8_unsafe", "prop_bool_v8_c16_unsafe", "prop_bool_v8_c24_unsafe", "prop_bool_v8_c32_unsafe", "prop_bool_v8_c40_unsafe", "prop_bool_v8_c46_unsafe", "prop_bool_v13_c13_unsafe", "prop_bool_v13_c26_unsafe", "prop_bool_v13_c39_unsafe", "prop_bool_v13_c52_unsafe", "prop_bool_v13_c65_unsafe", "prop_bool_v13_c78_unsafe", "prop_bool_v21_c21_unsafe", "prop_bool_v21_c42_unsafe", "prop_bool_v21_c62_unsafe", "prop_bool_v21_c84_unsafe", "prop_bool_v21_c105_unsafe", "prop_bool_v21_c126_unsafe", "prop_bool_v34_c34_unsafe", "prop_bool_v34_c68_unsafe", "prop_bool_v34_c102_unsafe", "prop_bool_v34_c136_unsafe", "prop_bool_v34_c170_unsafe", "prop_bool_v34_c204_unsafe", "prop_bool_v55_c55_unsafe", "prop_bool_v55_c110_unsafe", "prop_bool_v55_c165_unsafe", "prop_bool_v55_c220_unsafe", "prop_bool_v55_c275_unsafe", "prop_bool_v55_c330_unsafe", "prop_bool_v89_c89_unsafe", "prop_bool_v89_c178_unsafe", "prop_bool_v89_c267_unsafe", "prop_bool_v89_c356_unsafe", "prop_bool_v89_c445_unsafe", "prop_bool_v89_c534_unsafe", "prop_bool_v144_c144_unsafe", "prop_bool_v144_c288_unsafe", "prop_bool_v144_c432_unsafe", "prop_bool_v144_c576_unsafe", "prop_bool_v144_c720_unsafe", "prop_bool_v144_c864_unsafe"]

SAT_RELU_SORTED = []
for unsafe, safe in zip(SAT_RELU_UNSAFE_ORDERED, SAT_RELU_SAFE_ORDERED):
    SAT_RELU_SORTED.append(unsafe)
    SAT_RELU_SORTED.append(safe)

LIPSCHITZ_BOUNDED_SAFE_ORDERED = ["sll_2x4x4x1_case_3_safe","sll_2x4x4x1_case_4_safe","sll_2x4x4x1_case_5_safe","sll_3x4x4x1_case_3_safe","sll_3x4x4x1_case_4_safe","sll_3x4x4x1_case_5_safe","sll_4x4x4x1_case_3_safe","sll_4x4x4x1_case_4_safe","sll_4x4x4x1_case_5_safe","sll_2x8x8x1_case_3_safe","sll_2x8x8x1_case_4_safe","sll_2x8x8x1_case_5_safe","sll_3x8x8x1_case_3_safe","sll_3x8x8x1_case_4_safe","sll_3x8x8x1_case_5_safe","sll_4x8x8x1_case_3_safe","sll_4x8x8x1_case_4_safe","sll_4x8x8x1_case_5_safe","sll_2x12x12x1_case_3_safe","sll_2x12x12x1_case_4_safe","sll_2x12x12x1_case_5_safe","sll_3x12x12x1_case_3_safe","sll_3x12x12x1_case_4_safe","sll_3x12x12x1_case_5_safe","sll_4x12x12x1_case_3_safe","sll_4x12x12x1_case_4_safe","sll_4x12x12x1_case_5_safe","sll_2x16x16x1_case_3_safe","sll_2x16x16x1_case_4_safe","sll_2x16x16x1_case_5_safe","sll_3x16x16x1_case_3_safe","sll_3x16x16x1_case_4_safe","sll_3x16x16x1_case_5_safe","sll_4x16x16x1_case_3_safe","sll_4x16x16x1_case_4_safe","sll_4x16x16x1_case_5_safe","sll_2x20x20x1_case_3_safe","sll_2x20x20x1_case_4_safe","sll_2x20x20x1_case_5_safe","sll_3x20x20x1_case_3_safe","sll_3x20x20x1_case_4_safe","sll_3x20x20x1_case_5_safe","sll_4x20x20x1_case_3_safe","sll_4x20x20x1_case_4_safe","sll_4x20x20x1_case_5_safe","sll_2x24x24x1_case_3_safe","sll_2x24x24x1_case_4_safe","sll_2x24x24x1_case_5_safe","sll_3x24x24x1_case_3_safe","sll_3x24x24x1_case_4_safe","sll_3x24x24x1_case_5_safe","sll_4x24x24x1_case_3_safe","sll_4x24x24x1_case_4_safe","sll_4x24x24x1_case_5_safe"]

LIPSCHITZ_BOUNDED_UNSAFE_ORDERED = ["sll_2x4x4x1_case_0_unsafe","sll_2x4x4x1_case_1_unsafe","sll_2x4x4x1_case_2_unsafe","sll_3x4x4x1_case_0_unsafe","sll_3x4x4x1_case_1_unsafe","sll_3x4x4x1_case_2_unsafe","sll_4x4x4x1_case_0_unsafe","sll_4x4x4x1_case_1_unsafe","sll_4x4x4x1_case_2_unsafe","sll_2x8x8x1_case_0_unsafe","sll_2x8x8x1_case_1_unsafe","sll_2x8x8x1_case_2_unsafe","sll_3x8x8x1_case_0_unsafe","sll_3x8x8x1_case_1_unsafe","sll_3x8x8x1_case_2_unsafe","sll_4x8x8x1_case_0_unsafe","sll_4x8x8x1_case_1_unsafe","sll_4x8x8x1_case_2_unsafe","sll_2x12x12x1_case_0_unsafe","sll_2x12x12x1_case_1_unsafe","sll_2x12x12x1_case_2_unsafe","sll_3x12x12x1_case_0_unsafe","sll_3x12x12x1_case_1_unsafe","sll_3x12x12x1_case_2_unsafe","sll_4x12x12x1_case_0_unsafe","sll_4x12x12x1_case_1_unsafe","sll_4x12x12x1_case_2_unsafe","sll_2x16x16x1_case_0_unsafe","sll_2x16x16x1_case_1_unsafe","sll_2x16x16x1_case_2_unsafe","sll_3x16x16x1_case_0_unsafe","sll_3x16x16x1_case_1_unsafe","sll_3x16x16x1_case_2_unsafe","sll_4x16x16x1_case_0_unsafe","sll_4x16x16x1_case_1_unsafe","sll_4x16x16x1_case_2_unsafe","sll_2x20x20x1_case_0_unsafe","sll_2x20x20x1_case_1_unsafe","sll_2x20x20x1_case_2_unsafe","sll_3x20x20x1_case_0_unsafe","sll_3x20x20x1_case_1_unsafe","sll_3x20x20x1_case_2_unsafe","sll_4x20x20x1_case_0_unsafe","sll_4x20x20x1_case_1_unsafe","sll_4x20x20x1_case_2_unsafe","sll_2x24x24x1_case_0_unsafe","sll_2x24x24x1_case_1_unsafe","sll_2x24x24x1_case_2_unsafe","sll_3x24x24x1_case_0_unsafe","sll_3x24x24x1_case_1_unsafe","sll_3x24x24x1_case_2_unsafe","sll_4x24x24x1_case_0_unsafe","sll_4x24x24x1_case_1_unsafe","sll_4x24x24x1_case_2_unsafe"]

LIPSCHITZ_BOUNDED_ORDERED = [
    "sll_2x4x4x1_case_0_unsafe","sll_2x4x4x1_case_1_unsafe","sll_2x4x4x1_case_2_unsafe",
    "sll_2x4x4x1_case_3_safe","sll_2x4x4x1_case_4_safe","sll_2x4x4x1_case_5_safe",
    "sll_3x4x4x1_case_0_unsafe","sll_3x4x4x1_case_1_unsafe","sll_3x4x4x1_case_2_unsafe",
    "sll_3x4x4x1_case_3_safe","sll_3x4x4x1_case_4_safe","sll_3x4x4x1_case_5_safe",
    "sll_4x4x4x1_case_0_unsafe","sll_4x4x4x1_case_1_unsafe","sll_4x4x4x1_case_2_unsafe",
    "sll_4x4x4x1_case_3_safe","sll_4x4x4x1_case_4_safe","sll_4x4x4x1_case_5_safe",
    "sll_2x8x8x1_case_0_unsafe","sll_2x8x8x1_case_1_unsafe","sll_2x8x8x1_case_2_unsafe",
    "sll_2x8x8x1_case_3_safe","sll_2x8x8x1_case_4_safe","sll_2x8x8x1_case_5_safe",
    "sll_3x8x8x1_case_0_unsafe","sll_3x8x8x1_case_1_unsafe","sll_3x8x8x1_case_2_unsafe",
    "sll_3x8x8x1_case_3_safe","sll_3x8x8x1_case_4_safe","sll_3x8x8x1_case_5_safe",
    "sll_4x8x8x1_case_0_unsafe","sll_4x8x8x1_case_1_unsafe","sll_4x8x8x1_case_2_unsafe",
    "sll_4x8x8x1_case_3_safe","sll_4x8x8x1_case_4_safe","sll_4x8x8x1_case_5_safe",
    "sll_2x12x12x1_case_0_unsafe","sll_2x12x12x1_case_1_unsafe","sll_2x12x12x1_case_2_unsafe",
    "sll_2x12x12x1_case_3_safe","sll_2x12x12x1_case_4_safe","sll_2x12x12x1_case_5_safe",
    "sll_3x12x12x1_case_0_unsafe","sll_3x12x12x1_case_1_unsafe","sll_3x12x12x1_case_2_unsafe",
    "sll_3x12x12x1_case_3_safe","sll_3x12x12x1_case_4_safe","sll_3x12x12x1_case_5_safe",
    "sll_4x12x12x1_case_0_unsafe","sll_4x12x12x1_case_1_unsafe","sll_4x12x12x1_case_2_unsafe",
    "sll_4x12x12x1_case_3_safe","sll_4x12x12x1_case_4_safe","sll_4x12x12x1_case_5_safe",
    "sll_2x16x16x1_case_0_unsafe","sll_2x16x16x1_case_1_unsafe","sll_2x16x16x1_case_2_unsafe",
    "sll_2x16x16x1_case_3_safe","sll_2x16x16x1_case_4_safe","sll_2x16x16x1_case_5_safe",
    "sll_3x16x16x1_case_0_unsafe","sll_3x16x16x1_case_1_unsafe","sll_3x16x16x1_case_2_unsafe",
    "sll_3x16x16x1_case_3_safe","sll_3x16x16x1_case_4_safe","sll_3x16x16x1_case_5_safe",
    "sll_4x16x16x1_case_0_unsafe","sll_4x16x16x1_case_1_unsafe","sll_4x16x16x1_case_2_unsafe",
    "sll_4x16x16x1_case_3_safe","sll_4x16x16x1_case_4_safe","sll_4x16x16x1_case_5_safe",
    "sll_2x20x20x1_case_0_unsafe","sll_2x20x20x1_case_1_unsafe","sll_2x20x20x1_case_2_unsafe",
    "sll_2x20x20x1_case_3_safe","sll_2x20x20x1_case_4_safe","sll_2x20x20x1_case_5_safe",
    "sll_3x20x20x1_case_0_unsafe","sll_3x20x20x1_case_1_unsafe","sll_3x20x20x1_case_2_unsafe",
    "sll_3x20x20x1_case_3_safe","sll_3x20x20x1_case_4_safe","sll_3x20x20x1_case_5_safe",
    "sll_4x20x20x1_case_0_unsafe","sll_4x20x20x1_case_1_unsafe","sll_4x20x20x1_case_2_unsafe",
    "sll_4x20x20x1_case_3_safe","sll_4x20x20x1_case_4_safe","sll_4x20x20x1_case_5_safe",
    "sll_2x24x24x1_case_0_unsafe","sll_2x24x24x1_case_1_unsafe","sll_2x24x24x1_case_2_unsafe",
    "sll_2x24x24x1_case_3_safe","sll_2x24x24x1_case_4_safe","sll_2x24x24x1_case_5_safe",
    "sll_3x24x24x1_case_0_unsafe","sll_3x24x24x1_case_1_unsafe","sll_3x24x24x1_case_2_unsafe",
    "sll_3x24x24x1_case_3_safe","sll_3x24x24x1_case_4_safe","sll_3x24x24x1_case_5_safe",
    "sll_4x24x24x1_case_0_unsafe","sll_4x24x24x1_case_1_unsafe","sll_4x24x24x1_case_2_unsafe",
    "sll_4x24x24x1_case_3_safe","sll_4x24x24x1_case_4_safe","sll_4x24x24x1_case_5_safe"
    ]

POLY_APPROX_SAFE_ORDERED = ["poly_128_thresh_0_safe","poly_128_thresh_1_safe","poly_128_thresh_2_safe","poly_256_thresh_0_safe","poly_256_thresh_1_safe","poly_256_thresh_2_safe","poly_512_thresh_0_safe","poly_512_thresh_1_safe","poly_512_thresh_2_safe","poly_1024_thresh_0_safe","poly_1024_thresh_1_safe","poly_1024_thresh_2_safe","poly_16_16_thresh_0_safe","poly_16_16_thresh_1_safe","poly_16_16_thresh_2_safe","poly_32_32_thresh_0_safe","poly_32_32_thresh_1_safe","poly_32_32_thresh_2_safe","poly_64_64_thresh_0_safe","poly_64_64_thresh_1_safe","poly_64_64_thresh_2_safe","poly_128_128_thresh_0_safe","poly_128_128_thresh_1_safe","poly_128_128_thresh_2_safe","poly_8_8_8_thresh_0_safe","poly_8_8_8_thresh_1_safe","poly_8_8_8_thresh_2_safe","poly_16_16_16_thresh_0_safe","poly_16_16_16_thresh_1_safe","poly_16_16_16_thresh_2_safe","poly_32_32_32_thresh_0_safe","poly_32_32_32_thresh_1_safe","poly_32_32_32_thresh_2_safe","poly_64_64_64_thresh_0_safe","poly_64_64_64_thresh_1_safe","poly_64_64_64_thresh_2_safe","poly_4_4_4_4_thresh_0_safe","poly_4_4_4_4_thresh_1_safe","poly_4_4_4_4_thresh_2_safe","poly_8_8_8_8_thresh_0_safe","poly_8_8_8_8_thresh_1_safe","poly_8_8_8_8_thresh_2_safe","poly_16_16_16_16_thresh_0_safe","poly_16_16_16_16_thresh_1_safe","poly_16_16_16_16_thresh_2_safe","poly_32_32_32_32_thresh_0_safe","poly_32_32_32_32_thresh_1_safe","poly_32_32_32_32_thresh_2_safe"]


POLY_APPROX_UNSAFE_ORDERED = ["poly_128_thresh_3_unsafe","poly_128_thresh_4_unsafe","poly_128_thresh_5_unsafe","poly_256_thresh_3_unsafe","poly_256_thresh_4_unsafe","poly_256_thresh_5_unsafe","poly_512_thresh_3_unsafe","poly_512_thresh_4_unsafe","poly_512_thresh_5_unsafe","poly_1024_thresh_3_unsafe","poly_1024_thresh_4_unsafe","poly_1024_thresh_5_unsafe","poly_16_16_thresh_3_unsafe","poly_16_16_thresh_4_unsafe","poly_16_16_thresh_5_unsafe","poly_32_32_thresh_3_unsafe","poly_32_32_thresh_4_unsafe","poly_32_32_thresh_5_unsafe","poly_64_64_thresh_3_unsafe","poly_64_64_thresh_4_unsafe","poly_64_64_thresh_5_unsafe","poly_128_128_thresh_3_unsafe","poly_128_128_thresh_4_unsafe","poly_128_128_thresh_5_unsafe","poly_8_8_8_thresh_3_unsafe","poly_8_8_8_thresh_4_unsafe","poly_8_8_8_thresh_5_unsafe","poly_16_16_16_thresh_3_unsafe","poly_16_16_16_thresh_4_unsafe","poly_16_16_16_thresh_5_unsafe","poly_32_32_32_thresh_3_unsafe","poly_32_32_32_thresh_4_unsafe","poly_32_32_32_thresh_5_unsafe","poly_64_64_64_thresh_3_unsafe","poly_64_64_64_thresh_4_unsafe","poly_64_64_64_thresh_5_unsafe","poly_4_4_4_4_thresh_3_unsafe","poly_4_4_4_4_thresh_4_unsafe","poly_4_4_4_4_thresh_5_unsafe","poly_8_8_8_8_thresh_3_unsafe","poly_8_8_8_8_thresh_4_unsafe","poly_8_8_8_8_thresh_5_unsafe","poly_16_16_16_16_thresh_3_unsafe","poly_16_16_16_16_thresh_4_unsafe","poly_16_16_16_16_thresh_5_unsafe","poly_32_32_32_32_thresh_3_unsafe","poly_32_32_32_32_thresh_4_unsafe","poly_32_32_32_32_thresh_5_unsafe"]

POLY_APPROX_ORDERED = [
    "poly_128_thresh_0_safe", "poly_128_thresh_1_safe", "poly_128_thresh_2_safe",
    "poly_128_thresh_3_unsafe", "poly_128_thresh_4_unsafe", "poly_128_thresh_5_unsafe",
    "poly_256_thresh_0_safe", "poly_256_thresh_1_safe", "poly_256_thresh_2_safe",
    "poly_256_thresh_3_unsafe", "poly_256_thresh_4_unsafe", "poly_256_thresh_5_unsafe",
    "poly_512_thresh_0_safe", "poly_512_thresh_1_safe", "poly_512_thresh_2_safe",
    "poly_512_thresh_3_unsafe", "poly_512_thresh_4_unsafe", "poly_512_thresh_5_unsafe",
    "poly_1024_thresh_0_safe", "poly_1024_thresh_1_safe", "poly_1024_thresh_2_safe",
    "poly_1024_thresh_3_unsafe", "poly_1024_thresh_4_unsafe", "poly_1024_thresh_5_unsafe",
    "poly_16_16_thresh_0_safe", "poly_16_16_thresh_1_safe", "poly_16_16_thresh_2_safe",
    "poly_16_16_thresh_3_unsafe", "poly_16_16_thresh_4_unsafe", "poly_16_16_thresh_5_unsafe",
    "poly_32_32_thresh_0_safe", "poly_32_32_thresh_1_safe", "poly_32_32_thresh_2_safe",
    "poly_32_32_thresh_3_unsafe", "poly_32_32_thresh_4_unsafe", "poly_32_32_thresh_5_unsafe",
    "poly_64_64_thresh_0_safe", "poly_64_64_thresh_1_safe", "poly_64_64_thresh_2_safe",
    "poly_64_64_thresh_3_unsafe", "poly_64_64_thresh_4_unsafe", "poly_64_64_thresh_5_unsafe",
    "poly_128_128_thresh_0_safe", "poly_128_128_thresh_1_safe", "poly_128_128_thresh_2_safe",
    "poly_128_128_thresh_3_unsafe", "poly_128_128_thresh_4_unsafe", "poly_128_128_thresh_5_unsafe",
    "poly_8_8_8_thresh_0_safe", "poly_8_8_8_thresh_1_safe", "poly_8_8_8_thresh_2_safe",
    "poly_8_8_8_thresh_3_unsafe", "poly_8_8_8_thresh_4_unsafe", "poly_8_8_8_thresh_5_unsafe",
    "poly_16_16_16_thresh_0_safe", "poly_16_16_16_thresh_1_safe", "poly_16_16_16_thresh_2_safe",
    "poly_16_16_16_thresh_3_unsafe", "poly_16_16_16_thresh_4_unsafe", "poly_16_16_16_thresh_5_unsafe",
    "poly_32_32_32_thresh_0_safe", "poly_32_32_32_thresh_1_safe", "poly_32_32_32_thresh_2_safe",
    "poly_32_32_32_thresh_3_unsafe", "poly_32_32_32_thresh_4_unsafe", "poly_32_32_32_thresh_5_unsafe",
    "poly_64_64_64_thresh_0_safe", "poly_64_64_64_thresh_1_safe", "poly_64_64_64_thresh_2_safe",
    "poly_64_64_64_thresh_3_unsafe", "poly_64_64_64_thresh_4_unsafe", "poly_64_64_64_thresh_5_unsafe",
    "poly_4_4_4_4_thresh_0_safe", "poly_4_4_4_4_thresh_1_safe", "poly_4_4_4_4_thresh_2_safe",
    "poly_4_4_4_4_thresh_3_unsafe", "poly_4_4_4_4_thresh_4_unsafe", "poly_4_4_4_4_thresh_5_unsafe",
    "poly_8_8_8_8_thresh_0_safe", "poly_8_8_8_8_thresh_1_safe", "poly_8_8_8_8_thresh_2_safe",
    "poly_8_8_8_8_thresh_3_unsafe", "poly_8_8_8_8_thresh_4_unsafe", "poly_8_8_8_8_thresh_5_unsafe",
    "poly_16_16_16_16_thresh_0_safe", "poly_16_16_16_16_thresh_1_safe", "poly_16_16_16_16_thresh_2_safe",
    "poly_16_16_16_16_thresh_3_unsafe", "poly_16_16_16_16_thresh_4_unsafe", "poly_16_16_16_16_thresh_5_unsafe",
    "poly_32_32_32_32_thresh_0_safe", "poly_32_32_32_32_thresh_1_safe", "poly_32_32_32_32_thresh_2_safe",
    "poly_32_32_32_32_thresh_3_unsafe", "poly_32_32_32_32_thresh_4_unsafe", "poly_32_32_32_32_thresh_5_unsafe"
    ]

HOPFIELD_NETS_SAFE_ORDERED = ["softsign_w4_r1_case_1_safe","softsign_w4_r2_case_0_safe","softsign_w4_r3_case_0_safe","softsign_w4_r4_case_0_safe","softsign_w8_r1_case_1_safe","softsign_w8_r2_case_0_safe","softsign_w8_r3_case_0_safe","softsign_w8_r4_case_0_safe","softsign_w16_r1_case_1_safe","softsign_w16_r2_case_0_safe","softsign_w16_r3_case_0_safe","softsign_w16_r4_case_0_safe","softsign_w32_r1_case_1_safe","softsign_w32_r2_case_0_safe","softsign_w32_r3_case_0_safe","softsign_w32_r4_case_0_safe","softsign_w64_r1_case_1_safe","softsign_w64_r2_case_0_safe","softsign_w64_r3_case_0_safe","softsign_w64_r4_case_0_safe","tanh_w4_r1_case_1_safe","tanh_w4_r2_case_0_safe","tanh_w4_r3_case_0_safe","tanh_w4_r4_case_0_safe","tanh_w8_r1_case_1_safe","tanh_w8_r2_case_0_safe","tanh_w8_r3_case_0_safe","tanh_w8_r4_case_0_safe","tanh_w16_r1_case_1_safe","tanh_w16_r2_case_0_safe","tanh_w16_r3_case_0_safe","tanh_w16_r3_case_1_safe","tanh_w16_r4_case_0_safe","tanh_w16_r4_case_1_safe","tanh_w32_r1_case_1_safe","tanh_w32_r2_case_0_safe","tanh_w32_r3_case_0_safe","tanh_w32_r3_case_1_safe","tanh_w32_r4_case_0_safe","tanh_w32_r4_case_1_safe","tanh_w64_r1_case_1_safe","tanh_w64_r2_case_0_safe","tanh_w64_r3_case_0_safe","tanh_w64_r3_case_1_safe","tanh_w64_r4_case_0_safe","tanh_w64_r4_case_1_safe"]

HOPFIELD_NETS_UNSAFE_ORDERED = ["softsign_w4_r1_case_0_unsafe","softsign_w4_r2_case_1_unsafe","softsign_w4_r3_case_1_unsafe","softsign_w4_r4_case_1_unsafe","softsign_w8_r1_case_0_unsafe","softsign_w8_r2_case_1_unsafe","softsign_w8_r3_case_1_unsafe","softsign_w8_r4_case_1_unsafe","softsign_w16_r1_case_0_unsafe","softsign_w16_r2_case_1_unsafe","softsign_w16_r3_case_1_unsafe","softsign_w16_r4_case_1_unsafe","softsign_w32_r1_case_0_unsafe","softsign_w32_r2_case_1_unsafe","softsign_w32_r3_case_1_unsafe","softsign_w32_r4_case_1_unsafe","softsign_w64_r1_case_0_unsafe","softsign_w64_r2_case_1_unsafe","softsign_w64_r3_case_1_unsafe","softsign_w64_r4_case_1_unsafe","tanh_w4_r1_case_0_unsafe","tanh_w4_r2_case_1_unsafe","tanh_w4_r3_case_1_unsafe","tanh_w4_r4_case_1_unsafe","tanh_w8_r1_case_0_unsafe","tanh_w8_r2_case_1_unsafe","tanh_w8_r3_case_1_unsafe","tanh_w8_r4_case_1_unsafe","tanh_w16_r1_case_0_unsafe","tanh_w16_r2_case_1_unsafe","tanh_w32_r1_case_0_unsafe","tanh_w32_r2_case_1_unsafe","tanh_w64_r1_case_0_unsafe","tanh_w64_r2_case_1_unsafe"]

HOPFIELD_NETS_ORDERED = [
    "softsign_w4_r1_case_1_safe","softsign_w4_r2_case_0_safe","softsign_w4_r3_case_0_safe","softsign_w4_r4_case_0_safe",
    "softsign_w4_r1_case_0_unsafe","softsign_w4_r2_case_1_unsafe","softsign_w4_r3_case_1_unsafe","softsign_w4_r4_case_1_unsafe",
    "softsign_w8_r1_case_1_safe","softsign_w8_r2_case_0_safe","softsign_w8_r3_case_0_safe","softsign_w8_r4_case_0_safe",
    "softsign_w8_r1_case_0_unsafe","softsign_w8_r2_case_1_unsafe","softsign_w8_r3_case_1_unsafe","softsign_w8_r4_case_1_unsafe",
    "softsign_w16_r1_case_1_safe","softsign_w16_r2_case_0_safe","softsign_w16_r3_case_0_safe","softsign_w16_r4_case_0_safe",
    "softsign_w16_r1_case_0_unsafe","softsign_w16_r2_case_1_unsafe","softsign_w16_r3_case_1_unsafe","softsign_w16_r4_case_1_unsafe",
    "softsign_w32_r1_case_1_safe","softsign_w32_r2_case_0_safe","softsign_w32_r3_case_0_safe","softsign_w32_r4_case_0_safe",
    "softsign_w32_r1_case_0_unsafe","softsign_w32_r2_case_1_unsafe","softsign_w32_r3_case_1_unsafe","softsign_w32_r4_case_1_unsafe",
    "softsign_w64_r1_case_1_safe","softsign_w64_r2_case_0_safe","softsign_w64_r3_case_0_safe","softsign_w64_r4_case_0_safe",
    "softsign_w64_r1_case_0_unsafe","softsign_w64_r2_case_1_unsafe","softsign_w64_r3_case_1_unsafe","softsign_w64_r4_case_1_unsafe",
    "tanh_w4_r1_case_1_safe","tanh_w4_r1_case_0_unsafe","tanh_w4_r2_case_0_safe","tanh_w4_r2_case_1_unsafe","tanh_w4_r3_case_0_safe","tanh_w4_r3_case_1_unsafe","tanh_w4_r4_case_0_safe","tanh_w4_r4_case_1_unsafe",
    "tanh_w8_r1_case_1_safe","tanh_w8_r1_case_0_unsafe","tanh_w8_r2_case_0_safe","tanh_w8_r2_case_1_unsafe","tanh_w8_r3_case_0_safe","tanh_w8_r3_case_1_unsafe","tanh_w8_r4_case_0_safe","tanh_w8_r4_case_1_unsafe",
    "tanh_w16_r1_case_1_safe","tanh_w16_r1_case_0_unsafe","tanh_w16_r2_case_0_safe","tanh_w16_r2_case_1_unsafe","tanh_w16_r3_case_0_safe","tanh_w16_r3_case_1_safe","tanh_w16_r4_case_0_safe","tanh_w16_r4_case_1_safe",
    "tanh_w32_r1_case_1_safe","tanh_w32_r1_case_0_unsafe","tanh_w32_r2_case_0_safe","tanh_w32_r2_case_1_unsafe","tanh_w32_r3_case_0_safe","tanh_w32_r3_case_1_safe","tanh_w32_r4_case_0_safe","tanh_w32_r4_case_1_safe",
    "tanh_w64_r1_case_1_safe","tanh_w64_r1_case_0_unsafe","tanh_w64_r2_case_0_safe","tanh_w64_r2_case_1_unsafe","tanh_w64_r3_case_0_safe","tanh_w64_r3_case_1_safe","tanh_w64_r4_case_0_safe","tanh_w64_r4_case_1_safe"
    ]









