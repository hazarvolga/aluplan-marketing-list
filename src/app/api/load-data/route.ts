import { NextResponse } from 'next/server';
import { processExcelData } from '@/lib/excel-utils';
import * as fs from 'fs';
import * as path from 'path';

export async function GET() {
  try {
    // Path to the updated Excel file with new segment structure
    const filePath = path.join(process.cwd(), 'public', 'aluplan-list.xlsx');
    
    // Check if file exists
    if (!fs.existsSync(filePath)) {
      return NextResponse.json({
        success: false,
        error: 'Default data file not found',
        attemptedPath: filePath
      }, { status: 404 });
    }

    // Read the Excel file
    const buffer = fs.readFileSync(filePath);
    
    // Convert Buffer to ArrayBuffer
    const arrayBuffer = buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
    
    // Process the data
    const data = processExcelData(arrayBuffer);
    
    return NextResponse.json({
      success: true,
      data: data,
      message: `Loaded ${data.length} records successfully`
    });
  } catch (error) {
    console.error('Error loading default data:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to load default data',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
