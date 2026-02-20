# Comprehensive API Endpoint Test Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TESTING ALL API ENDPOINTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000"
$passed = 0
$failed = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET"
    )
    
    Write-Host "Testing: $Name" -NoNewline
    try {
        if ($Method -eq "GET") {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -ErrorAction Stop
        }
        
        if ($response.StatusCode -eq 200) {
            Write-Host " ✓ PASS" -ForegroundColor Green
            $script:passed++
            return $true
        } else {
            Write-Host " ✗ FAIL (Status: $($response.StatusCode))" -ForegroundColor Red
            $script:failed++
            return $false
        }
    } catch {
        Write-Host " ✗ FAIL (Error: $($_.Exception.Message))" -ForegroundColor Red
        $script:failed++
        return $false
    }
}

Write-Host "1. BASIC ENDPOINTS" -ForegroundColor Yellow
Write-Host "-------------------"
Test-Endpoint "Health Check" "$baseUrl/health"
Test-Endpoint "Root" "$baseUrl/"
Test-Endpoint "API Test" "$baseUrl/api/test"
Write-Host ""

Write-Host "2. ANALYTICS ENDPOINTS" -ForegroundColor Yellow
Write-Host "----------------------"
Test-Endpoint "Analytics (7d)" "$baseUrl/api/analytics?time_range=7d"
Test-Endpoint "Analytics (30d)" "$baseUrl/api/analytics?time_range=30d"
Test-Endpoint "Analytics Summary" "$baseUrl/api/analytics/summary"
Write-Host ""

Write-Host "3. HISTORY ENDPOINTS" -ForegroundColor Yellow
Write-Host "--------------------"
Test-Endpoint "History" "$baseUrl/api/history"
Test-Endpoint "History (paginated)" "$baseUrl/api/history?skip=0``&limit=10"
Write-Host ""

Write-Host "4. RL ENDPOINTS" -ForegroundColor Yellow
Write-Host "---------------"
Test-Endpoint "Q-Table" "$baseUrl/api/rl/qtable"
Test-Endpoint "Training History" "$baseUrl/api/rl/training-history"
Test-Endpoint "Reward Trend" "$baseUrl/api/rl/reward-trend"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TEST RESULTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host ""

if ($failed -eq 0) {
    Write-Host "✓ ALL TESTS PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ SOME TESTS FAILED" -ForegroundColor Red
    exit 1
}
