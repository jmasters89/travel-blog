document.addEventListener('DOMContentLoaded', function() {
  const journalForm = document.getElementById('journal-form');
  const journalContent = document.getElementById('journal-content');
  const journalEntries = document.getElementById('journal-entries');

  loadJournalEntries();

  journalForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const content = journalContent.value.trim();
    if (content) {
      createJournalEntry(content);
      journalContent.value = '';
    }
  });

  function loadJournalEntries() {
    fetch('/get-journal-entries')
      .then(response => response.json())
      .then(entries => {
        journalEntries.innerHTML = '';
        entries.forEach(entry => {
          journalEntries.appendChild(createEntryElement(entry));
        });
      })
      .catch(error => console.error('Error loading journal entries:', error));
  }

  function createJournalEntry(content) {
    fetch('/create-journal-entry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })
      .then(response => response.json())
      .then(entry => {
        journalEntries.prepend(createEntryElement(entry));
      })
      .catch(error => console.error('Error creating journal entry:', error));
  }

  function updateJournalEntry(id, content) {
    fetch('/update-journal-entry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, content })
    })
      .then(response => response.json())
      .then(updatedEntry => {
        const entryElement = document.getElementById(`entry-${id}`);
        entryElement.replaceWith(createEntryElement(updatedEntry));
      })
      .catch(error => console.error('Error updating journal entry:', error));
  }

  function deleteJournalEntry(id) {
    fetch('/delete-journal-entry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    })
      .then(response => response.json())
      .then(result => {
        if (result.success) {
          document.getElementById(`entry-${id}`).remove();
        }
      })
      .catch(error => console.error('Error deleting journal entry:', error));
  }

  let postCount = 0; // Global variable to keep track of post count

  function createEntryElement(entry) {
    postCount++; // Increment the post count

    const entryDiv = document.createElement('div');
    entryDiv.id = `entry-${entry._id}`;
    entryDiv.className = 'card mb-3 journal-entry';
    entryDiv.innerHTML = `
      <h3 class="card-header">Post #${postCount}</h3> <!-- Updated to show Post # -->
      <div class="card-body">
        <h6 class="card-subtitle mb-2 text-muted">By ${entry.author} on ${new Date(entry.timestamp).toLocaleString()}</h6>
        <p class="card-text">${entry.content}</p>
        <button class="btn btn-primary edit-btn" onclick="editEntry('${entry._id}', '${entry.content.replace(/'/g, "\\'")}')">
          <i class="fas fa-edit"></i> Edit
        </button>
        <button class="btn btn-danger delete-btn" onclick="deleteJournalEntry('${entry._id}')">
          <i class="fas fa-trash-alt"></i> Delete
        </button>
      </div>
    `;
    return entryDiv;
  }

  window.editEntry = function(id, content) {
    const newContent = prompt('Edit your entry:', content);
    if (newContent !== null && newContent.trim() !== '') {
      updateJournalEntry(id, newContent.trim());
    }
  };

  window.deleteJournalEntry = deleteJournalEntry;
});