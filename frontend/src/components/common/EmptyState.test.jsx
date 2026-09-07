import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { EmptyState } from './EmptyState'

describe('EmptyState', () => {
  it('renders helpful empty report copy', () => {
    render(<EmptyState title="No reports yet" description="Upload a sample lab report to get started." />)
    expect(screen.getByText('No reports yet')).toBeInTheDocument()
    expect(screen.getByText('Upload a sample lab report to get started.')).toBeInTheDocument()
  })
})