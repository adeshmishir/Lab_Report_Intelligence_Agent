import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { ResultTable } from './ResultTable'

describe('ResultTable', () => {
  it('renders normalized names, original names, missing data, and quality states', () => {
    render(
      <ResultTable results={[{
        test_name_normalized: 'HbA1c', test_name_original: 'A1C', value_numeric: 5.9,
        unit: null, reference_low: null, reference_high: null, data_quality: 'missing_unit',
      }]} />,
    )

    expect(screen.getByText('HbA1c')).toBeInTheDocument()
    expect(screen.getByText('Reported as: A1C')).toBeInTheDocument()
    expect(screen.getAllByText('Not provided')).toHaveLength(2)
    expect(screen.getByText('Missing unit')).toBeInTheDocument()
  })

  it('renders qualitative values and review copy', () => {
    render(<ResultTable results={[{
      test_name_normalized: 'Protein', test_name_original: 'Protein', value_text: 'Positive',
      data_quality: 'missing_reference_range',
    }]} />)

    expect(screen.getByText('Positive')).toBeInTheDocument()
    expect(screen.getByText('Missing range')).toBeInTheDocument()
  })
})