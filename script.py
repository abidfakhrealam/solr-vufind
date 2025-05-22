import pysolr

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/biblio', always_commit=False)

# Load language mappings
language_mappings = []
with open('language_mapping.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if '=' in line:
            old, new = line.strip().split('=')
            language_mappings.append((old.strip(), new.strip()))

batch_size = 1000
total_updated = 0

# Process each mapping separately
for old_lang, new_lang in language_mappings:
    query = f'{{!term f=language}}{old_lang}'
    start = 0
    updated_count = 0

    # Count matching documents
    total_docs = solr.search(query, rows=0).hits
    if total_docs == 0:
        print(f"No documents found for language='{old_lang}'")
        continue

    print(f"Processing language '{old_lang}' → '{new_lang}' ({total_docs} documents)")

    while updated_count < total_docs:
        results = solr.search(query, rows=batch_size, start=start)
        if not results.docs:
            break

        updates = []
        for doc in results:
            doc_id = doc.get('id')
            if not doc_id or 'language' not in doc:
                continue

            current_langs = doc['language']
            if isinstance(current_langs, str):
                current_langs = [current_langs]

            # Only update if the language list exactly matches ['old_lang']
            if current_langs == [old_lang]:
                updates.append({
                    "id": doc_id,
                    "language": {"set": [new_lang]}
                })

        if updates:
            try:
                solr.add(updates)
                updated_count += len(updates)
                print(f"  Updated {updated_count}/{total_docs} for '{old_lang}'")
            except Exception as e:
                print(f"  Error updating batch for '{old_lang}': {e}")

        start += batch_size

    total_updated += updated_count

# Final commit
solr.commit()
print(f"All updates completed. Total updated records: {total_updated}")
