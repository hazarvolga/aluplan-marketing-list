# Copilot Instructions for Aluplan Marketing Data Filter

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Next.js application built with TypeScript and TailwindCSS for filtering and analyzing marketing data from Excel files.

## Key Features
- Excel file processing using xlsx library
- Marketing data filtering by segments (Mautic, Sales Hub, V2022, V2023)
- Real-time data counting and statistics
- Search functionality across names, emails, and companies
- Export capabilities (CSV/Excel)
- Responsive design with modern UI

## Technical Stack
- Next.js 15 with App Router
- TypeScript
- TailwindCSS for styling
- xlsx library for Excel processing
- Lucide React for icons
- API routes for data processing

## Code Style Guidelines
- Use TypeScript for type safety
- Follow Next.js App Router conventions
- Use Tailwind utility classes for styling
- Implement proper error handling
- Use server-side processing for large datasets
- Keep components modular and reusable

## Data Structure
The application processes Excel files with the following structure:
- name: Contact name
- email: Email address
- company: Company name
- phone: Phone number
- segment: Comma-separated segment values (Mautic, Sales Hub Mevcut, V2022 ve eski, V2023 ve üzeri)

## Special Considerations
- Handle large Excel files efficiently
- Implement proper loading states
- Use Turkish language support where needed
- Maintain data privacy and security
- Optimize for performance with large datasets
