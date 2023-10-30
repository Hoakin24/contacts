import { Component } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { ContactsService } from 'src/app/services/contacts.service';
import { MessagesService } from 'src/app/services/messages.service';

@Component({
  selector: 'app-add',
  templateUrl: './add.component.html',
  styleUrls: ['./add.component.css']
})
export class AddComponent {
  add_user = {};
  response: any;
  err!: boolean;

  onClickSubmit(data: any) {
    if (data.favorite) {
      data.favorite = 1;
    } else {
      data.favorite = 0;
    }

    this.err = this.contactsService.dataValidation(data.name, data.email, data.telephone_number);
    if (this.err) {
      return;
    }

    this.add_user = {
      'name': data.name,
      'email': data.email,
      'telephone_number': data.telephone_number,
      'favorite': data.favorite
      
    };
    
    this.response = this.contactsService.addContact(this.add_user).subscribe({
      next: (data: any) => {
        this.messagesService.add(`ContactsService: ${data}`);
        window.location.reload();
      },
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
      });
     
  }

  constructor(private contactsService: ContactsService, private messagesService: MessagesService) {}
}
