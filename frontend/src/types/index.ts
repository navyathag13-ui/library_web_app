// ─── Resource ────────────────────────────────────────────────────────────────

export type ResourceStatus = 'available' | 'checked-out'

export interface Resource {
  id:              number
  title:           string
  author:          string
  category:        string
  description:     string | null
  isbn:            string | null
  totalCopies:     number
  availableCopies: number
  status:          ResourceStatus
  dateAdded:       string
  updatedAt:       string | null
  loans?:          Loan[]          // only present when fetched with include_loans
}

export interface ResourceFormData {
  title:       string
  author:      string
  category:    string
  description: string
  isbn:        string
  totalCopies: number
}

// ─── Loan ─────────────────────────────────────────────────────────────────────

export type LoanStatus = 'active' | 'returned' | 'overdue'

export interface Loan {
  id:            number
  resourceId:    number
  resourceTitle: string | null
  borrowerName:  string
  checkoutDate:  string
  dueDate:       string
  returnDate:    string | null
  status:        LoanStatus
  isOverdue:     boolean
}

export interface CheckoutFormData {
  borrowerName: string
  dueDate:      string   // ISO date string
}

// ─── Stats ───────────────────────────────────────────────────────────────────

export interface CategoryCount { name: string; count: number }

export interface Stats {
  total:      number
  available:  number
  checkedOut: number
  overdue:    number
  categories: CategoryCount[]
}

// ─── API pagination wrapper ───────────────────────────────────────────────────

export interface Paginated<T> {
  data:     T[]
  total:    number
  page:     number
  perPage:  number
  pages:    number
}

// ─── UI ───────────────────────────────────────────────────────────────────────

export interface FilterState {
  search:   string
  status:   ResourceStatus | ''
  category: string
  sortBy:   string
  sortOrder: 'asc' | 'desc'
}

export interface LoanFilterState {
  search: string
  status: LoanStatus | ''
}
