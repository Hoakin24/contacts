import { Component, Input } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

import { Contact } from 'src/app/interfaces/contact';
import { MessagesService } from 'src/app/services/messages.service';
import { ContactsService } from 'src/app/services/contacts.service';

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent {
  @Input() contact?: Contact; 
  err!: boolean;

  constructor(private route: ActivatedRoute, private contactsService: ContactsService, private location: Location, private messagesService: MessagesService) { }

  ngOnInit() {
    this.getContact();
  }

  getContact(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.contactsService.getContact(id).subscribe({
      next: (contact: any) => this.contact = contact,
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: CONTACT NOT FOUND ${err.error}`)
    });
  }

  goBack(): void {
    this.location.back();
  }

  save(): void {
    if (this.contact) {
      const id = Number(this.route.snapshot.paramMap.get('id'));

      this.err = this.contactsService.dataValidation(this.contact.name, this.contact.email, this.contact.telephone_number);
      if (this.err) {
        return;
      }

      this.contactsService.updateContact(id, this.contact).subscribe({
        next: (data: any) => this.messagesService.add(`ContactsService: Success ${data}`),
        error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
      });
    }
  }
}
