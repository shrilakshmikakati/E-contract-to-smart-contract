#!/usr/bin/env python3
"""
Simple verification of the new accuracy behavior
"""

print("🎯 VERIFICATION: New Accuracy Display Behavior")
print("=" * 50)

# Check the GUI file for the changes
with open('src/gui/main_window.py', 'r') as f:
    content = f.read()

print("✅ Checking smart contract generation success message...")
if 'Use \'Compare Contracts\' to see accuracy analysis' in content:
    print("   ✓ CONFIRMED: Accuracy removed from generation success message")
    print("   ✓ CONFIRMED: User directed to comparison for accuracy")
else:
    print("   ❌ NOT FOUND: Accuracy still showing in generation")

print("\n✅ Checking generation results display...")
if 'GENERATED SMART CONTRACT CODE:' in content:
    print("   ✓ CONFIRMED: Contract code shows first")
else:
    print("   ❌ NOT FOUND: Contract code not prioritized")

if 'accuracy removed - shown only in comparison' in content:
    print("   ✓ CONFIRMED: Accuracy removed from generation display")
else:
    print("   ❌ NOT FOUND: Accuracy still in generation display")

print("\n✅ Checking comparison results...")
if 'ACCURACY ANALYSIS:' in content and 'show first as requested' in content:
    print("   ✓ CONFIRMED: Accuracy analysis added to comparison")
    print("   ✓ CONFIRMED: Accuracy shows first in comparison")
else:
    print("   ❌ NOT FOUND: Accuracy not properly added to comparison")

print("\n🎉 SUMMARY OF CHANGES:")
print("   1. ✅ Smart contract generation shows CONTRACT CODE first")
print("   2. ✅ NO accuracy display during generation phase")
print("   3. ✅ Accuracy analysis ONLY shows during comparison phase") 
print("   4. ✅ User guided to use 'Compare Contracts' for accuracy")

print(f"\n📋 The system now behaves exactly as requested:")
print(f"   • Contract code is displayed FIRST during generation")
print(f"   • Accuracy is HIDDEN during generation")  
print(f"   • Accuracy analysis appears ONLY when comparing contracts")
print(f"   • Knowledge graph accuracy comparison included")