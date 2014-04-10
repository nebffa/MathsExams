import inspect
import os
import pickle
import random


class DummyPart:
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0

    def question_statement(self):
        return ''

    def solution_statement(self):
        return ''

    def sanity_check(self):
        pass


class QuestionPart:
    """Base class for all question parts.
    """
    is_root = False
    parent = None


    @classmethod
    def storage_paths(cls):
        """Return the paths that are involved in storing this class' questions.
        """
        class_path = inspect.getfile(cls)
        questions_folder, module_name = os.path.split(class_path)

        indices_folder = os.path.join(questions_folder, 'storage', 'indices')
        indices_name = '{module_name}_indices'.format(module_name=module_name)
        indices_path = os.path.join(indices_folder, indices_name)

        data_folder = os.path.join(questions_folder, 'storage', 'data')
        data_name = '{module_name}_{class_name}'.format(module_name=module_name, class_name=cls.__name__)
        data_path = os.path.join(data_folder, data_name)

        return indices_path, data_path


    @classmethod
    def store_question(cls):
        """Store all possible question numbers that have student-friendly values.
        """
        indices_path, data_path = cls.storage_paths()

        byte_indices = [0]
        with open(data_path, 'wb') as f:
            for question in cls.enumerate_questions():
                pickle.dump(question, f)
                byte_indices.append(f.tell())

        if os.path.exists(indices_path):
            with open(indices_path, 'rb') as f:
                cur_indices = pickle.load(f)
        else:
            cur_indices = {}

        cur_indices[cls.__name__] = byte_indices
        with open(indices_path, 'wb') as f:
            pickle.dump(cur_indices, f)


    @classmethod
    def scan_random_question(cls):
        """Return a random set of valid coefficients for this question.
        """
        indices_path, data_path = cls.storage_paths()

        with open(indices_path, 'rb') as f:
            all_indices = pickle.load(f)
            byte_indices = all_indices[cls.__name__]

        with open(data_path, 'rb') as f:
            question_number = random.randint(0, len(byte_indices) - 1)
            first_byte = byte_indices[question_number]
            last_byte = byte_indices[question_number + 1]

            f.seek(first_byte)
            pickled_question = f.read(last_byte - first_byte)

        return pickle.loads(pickled_question)


def root(cls):
    """A class decorator to specify a question root.

    """

    cls.is_root = True
    return cls


def is_child_of(parent):
    """A class decorator to specify a part's parent.

    """

    def decorator(cls):
        cls.parent = parent
        return cls
    return decorator


class PartTree:
    def __init__(self, cls):
        self.cls = cls
        self.children = []  # PartTrees of all the subparts

    def _find_parent(self, cls):
        if cls.parent == self.cls:  # the current node is the parent
            return self
        else:  # check if any of the current node's children is the parent
            for i in self.children:
                if i._find_parent(cls):
                    return i._find_parent(cls)

        raise RuntimeError('The class: {0} could not be located in the tree'.format(cls.__name__))

    def add_subpart(self, cls):
        child = PartTree(cls)
        parent = self._find_parent(cls)
        parent.children.append(child)


    def _instantiate_tree(self, depth=0, parent=None):
        if depth == 0:
            self.object = self.cls()
        else:
            self.object = self.cls(part=parent)

        for child in self.children:
            child._instantiate_tree(depth + 1, self.object)


    # does use the enumitem package, few hbox errors
    def _traversal_to_latex(self, depth=0):
        total_string = ''

        if self.object.question_statement() and depth == 0:
            total_string += r'<p>{0}</p>'.format(self.object.question_statement())
        elif self.object.question_statement():
            total_string += r'<p>{0}</p>'.format(self.object.question_statement())
        else:
            total_string += r'$ $'

        if self.children:
            total_string += ''.join(
                        i._traversal_to_latex(depth + 1) for i in self.children)

        return total_string


    def show_question(self):
        self._instantiate_tree()
        return self._traversal_to_latex()


def parse_structure(module):
    classes = []

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, QuestionPart):  # get all the question parts
            classes.append(obj)

    roots = [i for i in classes if i.is_root]
    no_dummy_parent = all([i.parent != DummyPart for i in classes])
    if len(roots) != 1 and no_dummy_parent:
        raise RuntimeError('There needs to be 1 and only 1 root in {0}'.format(module.__name__))
    root_part = roots[0]

    def invalid_part(cls):
        if not cls.is_root and cls.parent is None:
            return True
        else:
            return False

    root_node = PartTree(root_part)
    classes.remove(root_part)
    while classes:
        for i in range(len(classes)):
            cls = classes[i]
            if invalid_part(cls):
                raise ValueError('The part: {0} is neither the root part nor a subpart.'.format(cls.__name__))

            root_node.add_subpart(cls)
            classes.remove(cls)
            break  # we just removed something from the list, so we need to reset our iterator variable

    return root_node
