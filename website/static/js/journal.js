// Define these functions in the global scope
window.editJournalEntry = function(entryId) {
  const entryElement = document.getElementById(`entry-${entryId}`);
  const contentElement = entryElement.querySelector('.card-text');
  const originalContent = contentElement.innerHTML; // Store the entire inner HTML
  
  // Create a container for the edit form
  const editContainer = document.createElement('div');
  editContainer.className = 'edit-container';
  
  // Create and set up the textarea
  const textArea = document.createElement('textarea');
  textArea.value = contentElement.textContent.trim();
  textArea.className = 'form-control mb-2';
  editContainer.appendChild(textArea);
  
  // Create save button
  const saveButton = document.createElement('button');
  saveButton.textContent = 'Save';
  saveButton.className = 'btn btn-primary btn-sm mr-2';
  saveButton.onclick = function() {
    const newContent = textArea.value;
    window.updateJournalEntry(entryId, newContent);
  };
  
  // Create cancel button
  const cancelButton = document.createElement('button');
  cancelButton.textContent = 'Cancel';
  cancelButton.className = 'btn btn-secondary btn-sm';
  cancelButton.onclick = function() {
    contentElement.innerHTML = originalContent;
    window.restoreButtons(entryId);
  };
  
  // Create a container for the buttons
  const buttonsContainer = document.createElement('div');
  buttonsContainer.className = 'mt-2';
  buttonsContainer.appendChild(saveButton);
  buttonsContainer.appendChild(cancelButton);
  
  // Add buttons to the edit container
  editContainer.appendChild(buttonsContainer);
  
  // Replace the content with the edit form
  contentElement.innerHTML = '';
  contentElement.appendChild(editContainer);
  
  // Hide the photo during editing
  const photoElement = entryElement.querySelector('img');
  if (photoElement) {
    photoElement.style.display = 'none';
  }
  
  // Hide the original edit and delete buttons
  const originalButtons = entryElement.querySelectorAll('.edit-btn, .delete-btn');
  originalButtons.forEach(button => button.style.display = 'none');
};

window.deleteJournalEntry = function(id) {
  if (confirm('Are you sure you want to delete this entry?')) {
    fetch('/delete-journal-entry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(result => {
        if (result.success) {
          document.getElementById(`entry-${id}`).remove();
        } else {
          throw new Error(result.message || 'Failed to delete entry');
        }
      })
      .catch(error => {
        console.error('Error deleting journal entry:', error);
        alert(`Failed to delete entry: ${error.message}`);
      });
  }
};

// Move these functions to the global scope
window.updateJournalEntry = function(entryId, newContent) {
  fetch('/update-journal-entry', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: entryId, content: newContent }),
  })
  .then(response => {
    console.log('Response status:', response.status);
    return response.json().then(data => ({status: response.status, body: data}));
  })
  .then(({status, body}) => {
    console.log('Response body:', body);
    if (status === 200 && body._id) {
      const entryElement = document.getElementById(`entry-${entryId}`);
      entryElement.querySelector('.card-text').textContent = newContent;
      window.restoreButtons(entryId);
    } else {
      alert(`Failed to update entry. Status: ${status}, Error: ${JSON.stringify(body)}`);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred while updating the entry');
  });
};

window.restoreButtons = function(entryId) {
  const entryElement = document.getElementById(`entry-${entryId}`);
  const contentElement = entryElement.querySelector('.card-text');
  const actionsElement = entryElement.querySelector('.card-body');
  
  // Remove the edit container if it exists
  const editContainer = contentElement.querySelector('.edit-container');
  if (editContainer) {
    contentElement.removeChild(editContainer);
  }
  
  // Restore the original buttons
  let buttonsContainer = actionsElement.querySelector('.btn-container');
  if (!buttonsContainer) {
    buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'btn-container';
    actionsElement.appendChild(buttonsContainer);
  }
  
  buttonsContainer.innerHTML = `
    <button class="btn btn-primary edit-btn" onclick="editJournalEntry('${entryId}')">
      <i class="fas fa-edit"></i> Edit
    </button>
    <button class="btn btn-danger delete-btn" onclick="deleteJournalEntry('${entryId}')">
      <i class="fas fa-trash-alt"></i> Delete
    </button>
  `;
  
  // Show the photo if it exists
  const photoElement = entryElement.querySelector('img');
  if (photoElement) {
    photoElement.style.display = 'block';
  }
};

document.addEventListener('DOMContentLoaded', function() {
  const journalForm = document.getElementById('journal-form');
  const journalContent = document.getElementById('journal-content');
  const journalEntries = document.getElementById('journal-entries');
  const addWithPhotoBtn = document.getElementById('add-with-photo');
  const photoInput = document.getElementById('journal-photo');

  loadJournalEntries();

  if (journalForm) {
    journalForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const content = journalContent.value.trim();
      if (content) {
        createJournalEntry(content);
        journalContent.value = '';
        photoInput.value = ''; // Clear the file input
      }
    });

    addWithPhotoBtn.addEventListener('click', function() {
      photoInput.click();
    });

    photoInput.addEventListener('change', function() {
      if (photoInput.files.length > 0) {
        const content = journalContent.value.trim();
        if (content) {
          createJournalEntry(content, photoInput.files[0]);
          journalContent.value = '';
          photoInput.value = '';
        } else {
          alert('Please enter some content for your journal entry.');
        }
      }
    });
  }

  function loadJournalEntries() {
    fetch(`/get-journal-entries/${COUNTRY}`)
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw err; });
        }
        return response.json();
      })
      .then(entries => {
        journalEntries.innerHTML = '';
        entries.forEach(entry => {
          journalEntries.appendChild(createEntryElement(entry));
        });
      })
      .catch(error => {
        console.error('Error loading journal entries:', error);
        journalEntries.innerHTML = `<p>Failed to load journal entries. Error: ${JSON.stringify(error)}</p>`;
      });
  }

  function createJournalEntry(content, photo = null) {
    const formData = new FormData();
    formData.append('content', content);
    formData.append('country', COUNTRY);
    if (photo) {
      formData.append('photo', photo);
    }

    fetch('/create-journal-entry', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw err; });
        }
        return response.json();
      })
      .then(entry => {
        journalEntries.prepend(createEntryElement(entry));
      })
      .catch(error => {
        console.error('Error creating journal entry:', error);
        alert('Failed to create journal entry. Please try again.');
      });
  }

  function createEntryElement(entry) {
    console.log("Creating entry element:", entry);
    const entryDiv = document.createElement('div');
    entryDiv.id = `entry-${entry._id}`;
    entryDiv.className = 'card mb-3 journal-entry';
    entryDiv.innerHTML = `
      <div class="card-body">
        <h6 class="card-subtitle mb-2 text-muted">By ${entry.author_email} on ${new Date(entry.timestamp).toLocaleString()}</h6>
        ${entry.photo ? `<img src="${entry.photo}" alt="Journal entry photo" class="img-fluid mb-2">` : ''}
        <p class="card-text">${entry.content}</p>
        ${entry.is_author ? `
          <div class="btn-container">
            <button class="btn btn-primary edit-btn" onclick="editJournalEntry('${entry._id}')">
              <i class="fas fa-edit"></i> Edit
            </button>
            <button class="btn btn-danger delete-btn" onclick="deleteJournalEntry('${entry._id}')">
              <i class="fas fa-trash-alt"></i> Delete
            </button>
          </div>
        ` : ''}
      </div>
    `;
    console.log("Entry HTML:", entryDiv.innerHTML);
    return entryDiv;
  }
});