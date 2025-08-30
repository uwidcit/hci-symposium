# Group Files Directory Structure

This directory shows the expected structure for uploading group files using the `flask upload-group-files` command.

## Directory Structure
```
group_files_example/
├── Team Alpha/
│   ├── poster.pdf
│   └── presentation.pdf
├── Team Beta/
│   ├── poster.pdf
│   └── literature_review.pdf
└── Team Gamma/
    ├── poster.pdf
    └── presentation.pdf
```

## File Naming Conventions
- **Poster files**: Should contain "poster" in the filename (e.g., `poster.pdf`, `team_alpha_poster.pdf`)
- **Presentation files**: Should contain "presentation" or "lit" in the filename (e.g., `presentation.pdf`, `literature_review.pdf`)

## Usage
1. Create a directory with your group files organized as shown above
2. Run: `flask upload-group-files /path/to/your/group/files/directory`
3. The system will automatically match group names and upload the files

## Notes
- Only PDF files are supported
- Files are automatically renamed with UUID prefixes for security
- Group names must match exactly with the CSV data
