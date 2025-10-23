"""
BTP/MTP Allocation System - CORRECTED VERSION
Algorithm: Round-robin allocation based on sorted CGPA with mod n distribution
Each cycle MUST allocate exactly ONE student to each faculty
"""

import pandas as pd
import logging
from typing import Tuple, Dict
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('allocation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def count_faculties(df: pd.DataFrame) -> Tuple[list, int]:
    """
    Dynamically count faculties from columns after CGPA.
    
    Args:
        df: Input dataframe with student preferences
        
    Returns:
        Tuple of (faculty_list, faculty_count)
    """
    try:
        # Fixed columns are: Roll, Name, Email, CGPA
        faculty_columns = df.columns[4:].tolist()
        n_faculties = len(faculty_columns)
        logger.info(f"Detected {n_faculties} faculties: {faculty_columns}")
        return faculty_columns, n_faculties
    except Exception as e:
        logger.error(f"Error counting faculties: {str(e)}")
        raise


def allocate_students(input_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Allocate students to faculties using round-robin mod n algorithm.
    
    Algorithm:
    1. Sort students by CGPA in descending order (highest first)
    2. In each cycle, allocate EXACTLY n students (one to each faculty)
    3. Student at index i is allocated in cycle (i // n)
    4. Within each cycle, students try their preferences from 1 to n
    5. Each faculty gets exactly ONE student per complete cycle
    
    Args:
        input_file: Path to input CSV file
        
    Returns:
        Tuple of (allocation_df, preference_stats_df)
    """
    try:
        # Read input file
        logger.info(f"Reading input file: {input_file}")
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} students")
        
        # Count faculties dynamically
        faculty_columns, n_faculties = count_faculties(df)
        
        # Sort by CGPA in descending order (highest CGPA first)
        logger.info("Sorting students by CGPA in descending order")
        df_sorted = df.sort_values('CGPA', ascending=False).reset_index(drop=True)
        
        # Initialize tracking structures
        allocated = {}  # student_index -> faculty
        faculty_preference_stats = {fac: {f'Pref {i+1}': 0 for i in range(n_faculties)} 
                                    for fac in faculty_columns}
        
        # Calculate number of complete cycles
        n_students = len(df_sorted)
        n_complete_cycles = n_students // n_faculties
        n_remaining = n_students % n_faculties
        
        logger.info(f"Total students: {n_students}")
        logger.info(f"Complete cycles: {n_complete_cycles}")
        logger.info(f"Remaining students: {n_remaining}")
        
        # Allocation algorithm: Round-robin with mod n
        # Each cycle MUST allocate exactly n students (one per faculty)
        logger.info("Starting allocation process using mod n round-robin algorithm")
        
        # Process complete cycles
        for cycle in range(n_complete_cycles):
            logger.info(f"\n{'='*80}")
            logger.info(f"CYCLE {cycle + 1}/{n_complete_cycles}")
            logger.info(f"{'='*80}")
            
            # In this cycle, we need to allocate n students (indices: cycle*n to (cycle+1)*n - 1)
            cycle_start_idx = cycle * n_faculties
            cycle_end_idx = (cycle + 1) * n_faculties
            
            # Track which faculties have been allocated in this cycle
            faculties_allocated_in_cycle = set()
            
            # Get students for this cycle
            cycle_students = list(range(cycle_start_idx, cycle_end_idx))
            logger.info(f"Students in this cycle: indices {cycle_start_idx} to {cycle_end_idx - 1}")
            
            # For each student in this cycle, try to allocate to their highest preference
            # that hasn't been allocated yet in this cycle
            for student_idx in cycle_students:
                student_row = df_sorted.iloc[student_idx]
                
                # Try each preference from 1 to n
                for pref_num in range(1, n_faculties + 1):
                    # Find which faculty corresponds to this preference
                    for faculty in faculty_columns:
                        if student_row[faculty] == pref_num:
                            # Check if this faculty hasn't been allocated yet in this cycle
                            if faculty not in faculties_allocated_in_cycle:
                                # Allocate student to faculty
                                allocated[student_idx] = faculty
                                faculties_allocated_in_cycle.add(faculty)
                                
                                # Record preference statistics
                                faculty_preference_stats[faculty][f'Pref {pref_num}'] += 1
                                
                                logger.info(
                                    f"  Student {student_idx} ({student_row['Name']}, "
                                    f"CGPA: {student_row['CGPA']:.2f}) -> {faculty} "
                                    f"(Preference {pref_num})"
                                )
                                break
                    
                    # Break if student was allocated
                    if student_idx in allocated:
                        break
            
            # Verify that exactly n faculties were allocated in this cycle
            logger.info(f"\nCycle {cycle + 1} summary: {len(faculties_allocated_in_cycle)} faculties allocated")
            if len(faculties_allocated_in_cycle) != n_faculties:
                logger.warning(
                    f"WARNING: Expected {n_faculties} faculties to be allocated, "
                    f"but only {len(faculties_allocated_in_cycle)} were allocated!"
                )
        
        # Handle remaining students (partial cycle)
        if n_remaining > 0:
            logger.info(f"\n{'='*80}")
            logger.info(f"PARTIAL CYCLE - Remaining {n_remaining} students")
            logger.info(f"{'='*80}")
            
            remaining_start_idx = n_complete_cycles * n_faculties
            faculties_allocated_in_partial = set()
            
            for student_idx in range(remaining_start_idx, n_students):
                student_row = df_sorted.iloc[student_idx]
                
                # Try each preference from 1 to n
                for pref_num in range(1, n_faculties + 1):
                    # Find which faculty corresponds to this preference
                    for faculty in faculty_columns:
                        if student_row[faculty] == pref_num:
                            # Check if this faculty hasn't been allocated yet in partial cycle
                            if faculty not in faculties_allocated_in_partial:
                                # Allocate student to faculty
                                allocated[student_idx] = faculty
                                faculties_allocated_in_partial.add(faculty)
                                
                                # Record preference statistics
                                faculty_preference_stats[faculty][f'Pref {pref_num}'] += 1
                                
                                logger.info(
                                    f"  Student {student_idx} ({student_row['Name']}, "
                                    f"CGPA: {student_row['CGPA']:.2f}) -> {faculty} "
                                    f"(Preference {pref_num})"
                                )
                                break
                    
                    # Break if student was allocated
                    if student_idx in allocated:
                        break
        
        # Create output allocation dataframe
        logger.info("\nCreating allocation output")
        df_sorted['Allocated'] = df_sorted.index.map(
            lambda idx: allocated.get(idx, 'UNALLOCATED')
        )
        
        output_df = df_sorted[['Roll', 'Name', 'Email', 'CGPA', 'Allocated']]
        
        # Create preference statistics dataframe
        logger.info("Creating preference statistics")
        pref_stats_data = []
        for faculty in faculty_columns:
            row = {'Fac': faculty}
            for i in range(n_faculties):
                row[f'Count Pref {i+1}'] = faculty_preference_stats[faculty][f'Pref {i+1}']
            pref_stats_data.append(row)
        
        pref_stats_df = pd.DataFrame(pref_stats_data)
        
        # Log summary
        logger.info(f"\n{'='*80}")
        logger.info(f"ALLOCATION SUMMARY")
        logger.info(f"{'='*80}")
        logger.info(f"Total students: {len(df_sorted)}")
        logger.info(f"Allocated students: {len(allocated)}")
        logger.info(f"Unallocated students: {len(df_sorted) - len(allocated)}")
        
        # Count students per faculty
        faculty_counts = output_df['Allocated'].value_counts()
        logger.info(f"\nStudents per faculty:")
        for faculty in faculty_columns:
            count = faculty_counts.get(faculty, 0)
            logger.info(f"  {faculty}: {count} students")
        
        # Verify equal distribution for complete cycles
        expected_per_faculty = n_complete_cycles
        
        if n_remaining == 0:
            # All faculties should have exactly the same count
            all_same = len(set(faculty_counts[fac] for fac in faculty_columns if fac in faculty_counts)) == 1
            if all_same:
                logger.info(f"\n✓ SUCCESS: All faculties have equal allocation ({expected_per_faculty} students each)")
            else:
                logger.warning(f"\n✗ WARNING: Faculties have unequal allocation! Expected {expected_per_faculty} each.")
        
        return output_df, pref_stats_df
        
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error during allocation: {str(e)}")
        raise


def save_outputs(allocation_df: pd.DataFrame, pref_stats_df: pd.DataFrame,
                 allocation_file: str = 'output_btp_mtp_allocation.csv',
                 pref_stats_file: str = 'fac_preference_count.csv'):
    """
    Save allocation results to CSV files.
    
    Args:
        allocation_df: Student allocation dataframe
        pref_stats_df: Faculty preference statistics dataframe
        allocation_file: Output file path for allocations
        pref_stats_file: Output file path for preference statistics
    """
    try:
        logger.info(f"Saving allocation to {allocation_file}")
        allocation_df.to_csv(allocation_file, index=False)
        
        logger.info(f"Saving preference statistics to {pref_stats_file}")
        pref_stats_df.to_csv(pref_stats_file, index=False)
        
        logger.info("All outputs saved successfully")
    except Exception as e:
        logger.error(f"Error saving outputs: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        # Test with provided input file
        allocation_df, pref_stats_df = allocate_students('input_btp_mtp_allocation.csv')
        save_outputs(allocation_df, pref_stats_df)
        print("\nAllocation completed successfully!")
        
        # Display summary
        print("\n" + "="*80)
        print("FACULTY ALLOCATION COUNTS:")
        print("="*80)
        print(allocation_df['Allocated'].value_counts().sort_index())
        
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
        sys.exit(1)
