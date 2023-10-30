import { Component} from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { ContactsService } from 'src/app/services/contacts.service';
import { MessagesService } from 'src/app/services/messages.service';
import { Contact } from 'src/app/interfaces/contact';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent {
  contacts_list: Contact[] = [];
  current_page = "1"
  rows = "5"
  is_favorite_page: boolean = false

  constructor(private contactsService: ContactsService, private messagesService: MessagesService) {}
  
  ngOnInit(): void {
    this.paginate(this.current_page, this.rows);
  }

  getContacts(): void {
    this.is_favorite_page = false
    this.contactsService.getContacts().subscribe({
      next: (contacts: any) => {
        this.contacts_list = contacts;
        this.messagesService.add(`ContactsService: Contacts retrieved`);
      },
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
    });
  }

  getFavorites(): void {
    this.is_favorite_page = true
    this.contactsService.getFavorites().subscribe({
      next: (favorites: any) => {
        this.contacts_list = favorites;
        this.messagesService.add(`ContactsService: Favorites retrieved`);
      },
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
    });
  }

  deleteContact(contact: Contact): void {
    this.contactsService.deleteContact(contact.id).subscribe({
      next: (data: any) => {
        this.messagesService.add(`ContactsService: Deleted successfully`)
        this.paginate(this.current_page, this.rows);
      },
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
    });
    
  }

  isFavorite(contact: Contact): void {
    contact.favorite = !contact.favorite
    this.contactsService.isFavorite(contact.id, {'favorite': contact.favorite}).subscribe({
      next: (data: any) => this.messagesService.add(`ContactsService: Favorite changed`),
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
    });
  }

  searchContacts(text: string): void {
    this.contactsService.searchContacts(text, this.is_favorite_page).subscribe({
      next: (searched: any) => {
        this.contacts_list = searched;
        this.messagesService.add(`ContactsService: Searched contacts retrieved`);
      },
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
    });
  }

  paginate(page: string, rows: string): void {
    this.contactsService.paginate(Number(page), Number(rows)).subscribe({
      next: (paginated: any) => {
        this.contacts_list = paginated
        this.messagesService.add(`ContactsService: Paginated`);
      },
      error: (err: HttpErrorResponse) => this.messagesService.add(`ContactsService: ${err.error}`)
    });
  } 
}
