# from django.contrib.auth.base_user import BaseUserManager


# class customUserManager(BaseUserManager):
    
#     def create_user(self,phone_number,password=None,**extra_dict_values):

#         if not phone_number:
#             raise ValueError("Phone number is not given,Extremmly required.")
        
#         extra_dict_values['user_email']= self.normalize_email(extra_dict_values['user_email'])

#         extra_dict_values.setdefault('is_active',True)

#         user=self.model(phone_number=phone_number,**extra_dict_values) 
#         #instead hardcodded: user=customUser(phone_number=phone_number,**extra_dict_values) ;;will create a customUser object

#         user.set_passward(password)  #it is convert passward in hasing.

#         user.save()  #user.save(using =self.db) is to specify that the data is to be stored in which database.

#         return user
    

#     def create_superuser(self,phone_number,password=None,**extra_dict_values):

#         #is_staff(for admin access) and is_superuser(for availing the superuser previledges)
#         # should be True for the super user.

#         extra_dict_values.setdefault('is_staff',True) 
       
#         extra_dict_values.setdefault('is_active',True)

#         extra_dict_values.setdefault('is_superuser',True)

#         return self.createUser(phone_number,password,**extra_dict_values)